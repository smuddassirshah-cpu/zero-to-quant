#!/usr/bin/env python3
"""Concept audit, round 1 (blind): contests level 4 (l13 to l16, review-4, homework-4).

Parts, all run on the content's own code and numbers:
  A. every code widget: the solution passes its hidden tests, the starter fails;
  B. every `feedback.byKey.test-N` line: the mistake the line names, written as a real
     submission, must pass tests 1..N-1 and fail first at test N;
  C. stated numbers and ordering arguments, recomputed (decay rule, exchange argument,
     ICPC penalty, the D or E split curve, binomial counts, logs);
  D. optional page run: with `--pyodide <pkgs>` every solution is also run in Pyodide 0.27.7
     under node, with the page's recursion limit of 3,000, and each test must finish in 5 s.

The harness copies app/js/engine/widgets/code.js: prelude then learner code in one module
namespace, loaded once; each test runs its setup then evaluates its call in that namespace;
`equal` treats lists and tuples alike, `isclose` is math.isclose(rel 1e-9, abs 1e-12); the key
is `test-N` for the first failing test (a wrong value, an exception or 5 s without an answer)
and `error` only when the code does not load. Native CPython is faster than Pyodide, so a
mutant that runs past 5 s here also does on the page.

A check labelled FINDING n holds a claim the content makes that is false; it stays failing
until the content is fixed, and it is finding n of docs/reviews/audit-contests-4.md.
Exit 0 when every check holds. Run from the repository root:
  python3 docs/reports/contests-L4-concepts.py [--pyodide <pkgs>]
"""
import itertools, json, math, os, random, signal, subprocess, sys, tempfile, time

sys.setrecursionlimit(3000)          # the page's limit (app/js/screens/drill-worker.js, RECURSION_LIMIT)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'contests')
FAIL, N = [], [0]


def ck(label, cond, detail=''):
    N[0] += 1
    if not cond:
        FAIL.append(label + (' :: ' + str(detail) if detail != '' else ''))


def load(name):
    with open(os.path.join(ROOT, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


L13, L14, L15, L16 = load('l13-virtual-contest'), load('l14-which-first'), load('l15-debugging-under-time'), load('l16-upsolving')
R4, H4 = load('review-4'), load('homework-4')


# ---------------------------------------------------------------- the harness
class TimeUp(BaseException):
    pass


def _alarm(sig, frm):
    raise TimeUp()


signal.signal(signal.SIGALRM, _alarm)


def _same(x, y):
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    return bool(x == y)


def _close(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def run(w, code, limit=5):
    """First failing key: None (all pass), 'error' (does not load) or 'test-N'. Also the slowest test's seconds."""
    g = {'__name__': '__main__'}
    try:
        exec(w.get('prelude', ''), g)
        exec(code, g)
    except BaseException:
        return 'error', 0.0
    slow = 0.0
    for i, t in enumerate(w['tests']):
        ok = False
        t0 = time.time()
        signal.alarm(limit)
        try:
            if t.get('setup'):
                exec(t['setup'], g)
            a = eval(t['call'], g)
            e = eval(str(t['expect']), g)
            ok = _close(a, e) if t.get('compare') == 'isclose' else _same(a, e)
        except TimeUp:
            ok = False
        except BaseException:
            ok = False
        finally:
            signal.alarm(0)
        slow = max(slow, time.time() - t0)
        if not ok:
            return 'test-%d' % (i + 1), slow
    return None, slow


WIDGETS = {
    'l13 A peaks': (L13['screens'][3], 10),
    'l13 B shortest_cover': (L13['screens'][4], 9),
    'l13 C min_capacity': (L13['screens'][5], 11),
    'l13 D grid_moves': (L13['screens'][6], 9),
    'l14 decayed_score': (L14['screens'][4], 8),
    'l14 icpc_rank_key': (L14['screens'][5], 7),
    'l14 best_order': (L14['screens'][10], 6),
    'l15 last_occurrence': (L15['screens'][3], 7),
    'l15 count_inversions_small': (L15['screens'][4], 7),
    'l15 solve_all': (L15['screens'][5], 6),
    'l15 smallest_failing': (L15['screens'][9], 7),
    'l16 equal_thirds': (L16['screens'][3], 9),
    'l16 mistakes_summary': (L16['screens'][5], 8),
    'hw4 desks_after_cut': (H4['items'][0], 8),
    'hw4 max_profit_k': (H4['items'][1], 8),
    'hw4 widest_gap': (H4['items'][2], 8),
}
# every code widget in scope is listed above
n_code = sum(1 for d in (L13, L14, L15, L16, R4, H4) for it in (d.get('screens') or []) + (d.get('quiz') or []) + (d.get('items') or [])
             if it.get('widget', {}).get('kind') == 'code')
ck('code widgets in scope: 16, all listed', n_code == 16 == len(WIDGETS), n_code)
ck('all code widgets are Python (no C++ at this level)', all(s['widget'].get('language') == 'python' for s, _ in WIDGETS.values()))

# ---------------------------------------------------------------- A. solutions and starters
STARTER_KEY = {'l15 last_occurrence': 'test-4', 'l15 count_inversions_small': 'test-3', 'l15 solve_all': 'test-2'}
for name, (item, ntests) in WIDGETS.items():
    w = item['widget']
    ck('A %s: %d hidden tests' % (name, ntests), len(w['tests']) == ntests, len(w['tests']))
    key, slow = run(w, w['solution'])
    ck('A %s: solution passes every test' % name, key is None, key)
    ck('A %s: solution slowest test under 1 s natively' % name, slow < 1.0, round(slow, 2))
    key, _ = run(w, w['starter'])
    ck('A %s: starter fails' % name, key is not None, key)
    if name in STARTER_KEY:   # the three "fix this submission" starters fail where the lesson's verdict says
        ck('A %s: starter first fails at %s, as the screen says' % (name, STARTER_KEY[name]), key == STARTER_KEY[name], key)
    else:
        ck('A %s: bare starter fails at test 1' % name, key == 'test-1', key)
    for ex in w.get('examples', []):
        ck('A %s: example is one of the hidden tests' % name, any(t['call'] == ex['call'] and str(t['expect']) == str(ex['expect']) for t in w['tests']))


# ---------------------------------------------------------------- B. byKey lines against real mutants
def mutant(name, label, code, want, finding=None):
    item, _ = WIDGETS[name]
    w = item['widget']
    key, _ = run(w, code)
    tag = ('FINDING %s ' % finding) if finding else 'B '
    ck('%s%s: "%s" first fails at %s' % (tag, name, label, want), key == want, key)
    return key


def keys_of(name):
    return sorted(k for k in WIDGETS[name][0]['feedback'].get('byKey', {}))


# the lines this script covers are exactly the lines the content has
EXPECT_KEYS = {
    'l13 A peaks': ['test-2', 'test-3', 'test-4', 'test-5', 'test-6'],
    'l13 B shortest_cover': ['test-3', 'test-5', 'test-8', 'test-9'],
    'l13 C min_capacity': ['test-10', 'test-11', 'test-2', 'test-4'],
    'l13 D grid_moves': ['test-1', 'test-2', 'test-3', 'test-9'],
    'l14 decayed_score': ['test-2', 'test-7'],
    'l14 icpc_rank_key': ['test-1', 'test-5'],
    'l14 best_order': ['test-2', 'test-3', 'test-4'],
    'l15 last_occurrence': ['test-3', 'test-4'],
    'l15 count_inversions_small': ['test-3', 'test-6'],
    'l15 solve_all': ['test-2', 'test-3'],
    'l15 smallest_failing': ['test-3', 'test-6', 'test-7'],
    'l16 equal_thirds': ['test-2', 'test-5', 'test-6', 'test-8'],
    'l16 mistakes_summary': ['test-1', 'test-2', 'test-6', 'test-7'],
    'hw4 desks_after_cut': ['test-2', 'test-4', 'test-7'],
    'hw4 max_profit_k': ['test-3', 'test-4', 'test-6', 'test-8'],
    'hw4 widest_gap': ['test-1', 'test-4', 'test-8'],
}
for name, want in EXPECT_KEYS.items():
    ck('B %s: byKey lines are %s' % (name, want), keys_of(name) == sorted(want), keys_of(name))
ck('B no `error` or `compile` byKey line at this level', not any(k in ('error', 'compile') for n in WIDGETS for k in keys_of(n)))

# ---- l13 A peaks
mutant('l13 A peaks', 'reads closes[1] before the loop (n = 1 crashes)', '''
def peaks(closes):
    first, second = closes[0], closes[1]
    return sum(1 for i in range(1, len(closes) - 1) if closes[i] > closes[i - 1] and closes[i] > closes[i + 1])
''', 'test-2')
mutant('l13 A peaks', 'counts the last day when it is above its one neighbour', '''
def peaks(closes):
    n = len(closes)
    return sum(1 for i in range(1, n) if closes[i] > closes[i - 1] and (i == n - 1 or closes[i] > closes[i + 1]))
''', 'test-3')
mutant('l13 A peaks', 'counts the first day when it is above its one neighbour', '''
def peaks(closes):
    n = len(closes)
    return sum(1 for i in range(0, n - 1) if (i == 0 or closes[i] > closes[i - 1]) and closes[i] > closes[i + 1])
''', 'test-4')
mutant('l13 A peaks', '>= on one side only', '''
def peaks(closes):
    return sum(1 for i in range(1, len(closes) - 1) if closes[i] > closes[i - 1] and closes[i] >= closes[i + 1])
''', 'test-6')
# the explain's "`>=` slip", written on both sides, stops one test earlier, on the flat closes, where there is no line
mutant('l13 A peaks', '>= on both sides lands on the flat-closes line test-5 (fix pass)', '''
def peaks(closes):
    return sum(1 for i in range(1, len(closes) - 1) if closes[i] >= closes[i - 1] and closes[i] >= closes[i + 1])
''', 'test-5', finding=1)

# ---- l13 B shortest_cover
mutant('l13 B shortest_cover', 'returns infinity when nothing covers', '''
def shortest_cover(tickers, needed):
    need = set(needed); count = {}; have = 0; best = float("inf"); left = 0
    for right, t in enumerate(tickers):
        if t in need:
            count[t] = count.get(t, 0) + 1
            if count[t] == 1: have += 1
        while have == len(need):
            best = min(best, right - left + 1)
            u = tickers[left]
            if u in need:
                count[u] -= 1
                if count[u] == 0: have -= 1
            left += 1
    return best
''', 'test-3')
mutant('l13 B shortest_cover', 'compares with len(needed), not len(set(needed))', '''
def shortest_cover(tickers, needed):
    need = set(needed); count = {}; have = 0; best = -1; left = 0
    for right, t in enumerate(tickers):
        if t in need:
            count[t] = count.get(t, 0) + 1
            if count[t] == 1: have += 1
        while have == len(needed):
            if best == -1 or right - left + 1 < best: best = right - left + 1
            u = tickers[left]
            if u in need:
                count[u] -= 1
                if count[u] == 0: have -= 1
            left += 1
    return best
''', 'test-5')
RESTART = '''
def shortest_cover(tickers, needed):
    need = set(needed); n = len(tickers); best = -1
    %s
    for left in range(n):
        seen = set()
        for right in range(left, n):
            t = tickers[right]
            if t in need:
                seen.add(t)
                if len(seen) == len(need):
                    if best == -1 or right - left + 1 < best: best = right - left + 1
                    break
    return best
'''
mutant('l13 B shortest_cover', 'restart at every left end', RESTART % '', 'test-8')
mutant('l13 B shortest_cover', 'restart at every left end on a plain copy of the tape (reads not counted)', RESTART % 'tickers = list(tickers)', 'test-9')

# ---- l13 C can_ship / min_capacity
SOL_C = WIDGETS['l13 C min_capacity'][0]['widget']['solution']
mutant('l13 C min_capacity', 'can_ship left unwritten, min_capacity with its own inline check', '''
def can_ship(weights, k, cap):
    ...

def min_capacity(weights, k):
    def ok(cap):
        days, load = 1, 0
        for w in weights:
            if load + w > cap:
                days += 1; load = 0
            load += w
        return days <= k
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid): hi = mid
        else: lo = mid + 1
    return lo
''', 'test-2')
mutant('l13 C min_capacity', 'an order heavier than the van rides alone (new day only when the van is not empty)', '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if load + w > cap and load > 0:
            days += 1; load = 0
        load += w
    return days <= k

def min_capacity(weights, k):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, k, mid): hi = mid
        else: lo = mid + 1
    return lo
''', 'test-4')
# a greedy with no explicit "heavier than the van" test is not a mistake on test 4: the order still opens a second day
key, _ = run(WIDGETS['l13 C min_capacity'][0]['widget'], SOL_C.replace('        if w > cap:\n            return False\n', ''))
ck('B l13 C: the solution without its `w > cap` line still passes all 11 tests', key is None, key)
mutant('l13 C min_capacity', 'scan capacities upwards from the heaviest order', '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if w > cap: return False
        if load + w > cap:
            days += 1; load = 0
        load += w
    return days <= k

def min_capacity(weights, k):
    cap = max(weights)
    while not can_ship(weights, k, cap):
        cap += 1
    return cap
''', 'test-10')
mutant('l13 C min_capacity', 'scan upwards with an inline check (no can_ship calls to count)', '''
def can_ship(weights, k, cap):
    days, load = 1, 0
    for w in weights:
        if w > cap: return False
        if load + w > cap:
            days += 1; load = 0
        load += w
    return days <= k

def min_capacity(weights, k):
    cap = max(weights)
    while True:
        days, load = 1, 0
        for w in weights:
            if load + w > cap:
                days += 1; load = 0
            load += w
        if days <= k: return cap
        cap += 1
''', 'test-11')

# ---- l13 D grid_moves
mutant('l13 D grid_moves', 'ignores the arrows', '''
from collections import deque
def grid_moves(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]; dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        if (r, c) == (rows - 1, cols - 1): return dist[r][c]
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1; q.append((nr, nc))
    return -1
''', 'test-1')
mutant('l13 D grid_moves', 'checks for the target only when pushing a neighbour', '''
from collections import deque
STEP = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
def grid_moves(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]; dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        cell = grid[r][c]
        for dr, dc in ([STEP[cell]] if cell in STEP else STEP.values()):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                if (nr, nc) == (rows - 1, cols - 1): return dist[nr][nc]
                q.append((nr, nc))
    return -1
''', 'test-3')
mutant('l13 D grid_moves', 'a queue with no visited marks (cells revisited)', '''
from collections import deque
STEP = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
def grid_moves(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque([(0, 0, 0)])
    while q:
        r, c, d = q.popleft()
        if d > rows * cols: return -1
        if (r, c) == (rows - 1, cols - 1): return d
        cell = grid[r][c]
        for dr, dc in ([STEP[cell]] if cell in STEP else STEP.values()):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                q.append((nr, nc, d + 1))
    return -1
''', 'test-9')

# ---- l14 decayed_score
mutant('l14 decayed_score', 'no floor', '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    return value - per_minute * minute - per_wrong * wrong
''', 'test-2')
mutant('l14 decayed_score', 'a floor of 0 treated as no floor', '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    s = value - per_minute * minute - per_wrong * wrong
    return max(floor * value, s) if floor else s
''', 'test-7')
# test-6 says "Apply the floor after both costs": the two ways of flooring too early both stop at test 2
mutant('l14 decayed_score', 'floor applied before the attempt cost lands on test-2 (fix pass: line moved there)', '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    return max(floor * value, value - per_minute * minute) - per_wrong * wrong
''', 'test-2', finding=2)
mutant('l14 decayed_score', 'floor applied before the time cost lands on test-2 (fix pass: line moved there)', '''
def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):
    return max(floor * value, value - per_wrong * wrong) - per_minute * minute
''', 'test-2', finding=2)

# ---- l14 icpc_rank_key
mutant('l14 icpc_rank_key', 'charges rejections on unsolved problems', '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        penalty += per_wrong * wrong
        if minute is not None:
            solved += 1; penalty += minute
    return (-solved, penalty)
''', 'test-1')
# test-2 ("whatever the rejections") names the same slip, which has already stopped at test 1
mutant('l14 icpc_rank_key', 'charges rejections on unsolved problems lands on test-1 (fix pass: test-2 line deleted)', '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        penalty += per_wrong * wrong
        if minute is not None:
            solved += 1; penalty += minute
    return (-solved, penalty)
''', 'test-1', finding=3)
# test-7: every wrong key order or sign already fails test 1
for label, ret in [('solved count not negated', '(solved, penalty)'), ('penalty first', '(penalty, -solved)'), ('penalty negated', '(-solved, -penalty)')]:
    mutant('l14 icpc_rank_key', label + ' lands on test-1 (fix pass: test-7 line deleted)', '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        if minute is not None:
            solved += 1; penalty += minute + per_wrong * wrong
    return %s
''' % ret, 'test-1', finding=3)
# the slip the tests do catch without a line: `if minute:` drops a solve at minute 0 (test 5)
mutant('l14 icpc_rank_key', '`if minute:` drops a solve at minute 0 (fix pass: test-5 line added)', '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        if minute:
            solved += 1; penalty += minute + per_wrong * wrong
    return (-solved, penalty)
''', 'test-5')

# ---- l14 best_order
PRE14 = ''
mutant('l14 best_order', 'points per minute order, no search', '''
def best_order(problems, minutes):
    order = sorted(problems, key=lambda p: (-p[1] / p[2], p[0]))
    clock, total = 0, 0
    for name, value, time in order:
        clock += time
        if clock <= minutes:
            total += decayed_score(value, clock, 0, value / 250, 50, 0.3)
    return total, [p[0] for p in order]
''', 'test-2')
mutant('l14 best_order', 'no sort by name before the permutations', '''
from itertools import permutations
def best_order(problems, minutes):
    best_total, best_names = -1, None
    for order in permutations(problems):
        clock, total = 0, 0
        for name, value, time in order:
            clock += time
            if clock <= minutes:
                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)
        if total > best_total:
            best_total, best_names = total, [p[0] for p in order]
    return best_total, best_names
''', 'test-3')
mutant('l14 best_order', 'best total starts at 0, so a round that scores 0 keeps no order', '''
from itertools import permutations
def best_order(problems, minutes):
    best_total, best_names = 0, None
    for order in permutations(sorted(problems)):
        clock, total = 0, 0
        for name, value, time in order:
            clock += time
            if clock <= minutes:
                total += decayed_score(value, clock, 0, value / 250, 50, 0.3)
        if total > best_total:
            best_total, best_names = total, [p[0] for p in order]
    return best_total, best_names
''', 'test-4')

# ---- l15 last_occurrence
mutant('l15 last_occurrence', 'checks xs[-1] first (empty list crashes)', '''
def last_occurrence(xs, x):
    if xs[-1] == x:
        return len(xs) - 1
    for i in range(len(xs) - 2, -1, -1):
        if xs[i] == x:
            return i
    return -1
''', 'test-3')
# test-4 is the starter itself (part A)

# ---- l15 count_inversions_small: test-3 is the starter; test-6 by a wrong repair of the tie bug
mutant('l15 count_inversions_small', 'removes repeated values, keeps >=', '''
def count_inversions_small(xs):
    xs = list(dict.fromkeys(xs))
    n = len(xs)
    return sum(1 for i in range(n) for j in range(i + 1, n) if xs[i] >= xs[j])
''', 'test-6')

# ---- l15 solve_all: test-2 is the starter. test-6 names a module-level set that survives a call;
# the tests share one loaded module (code.js loads the code once), so any such set shows by test 3
LEAK = '''
seen = set()

def solve_all(text):
    data = text.split(); t = int(data[0]); pos = 1; out = []
    for case in range(t):
        n = int(data[pos]); pos += 1
        %s
        for s in data[pos:pos + n]:
            seen.add(s)
        pos += n
        out.append(len(seen))
    return out
'''
k1 = mutant('l15 solve_all', 'module-level set, never emptied (the starter)', LEAK % 'pass', 'test-2')
mutant('l15 solve_all', 'module-level set emptied between cases but not between calls lands on test-3 (fix pass: line added)', LEAK % 'if case: seen.clear()', 'test-3', finding=4)

# ---- l15 smallest_failing
mutant('l15 smallest_failing', 'tries lengths 1 and 2 only', '''
def smallest_failing(fast, brute, gen, seed):
    for n in range(1, 3):
        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)
        if case is not None:
            return case
    return None
''', 'test-3')
# the line's own words, "not only the longest": that submission stops at test 1
mutant('l15 smallest_failing', 'tries only the longest length, 8, stops at test-1 (fix pass: test-3 line now names stopping at length 2)', '''
def smallest_failing(fast, brute, gen, seed):
    return stress(fast, brute, lambda rng: gen(rng, 8), 200, seed)
''', 'test-1', finding=5)
mutant('l15 smallest_failing', 'ignores gen and always draws values 1 to 3', '''
def smallest_failing(fast, brute, gen, seed):
    for n in range(1, 9):
        case = stress(fast, brute, lambda rng: gen_list(rng, n), 200, seed)
        if case is not None:
            return case
    return None
''', 'test-6')
mutant('l15 smallest_failing', 'stops at length 4', '''
def smallest_failing(fast, brute, gen, seed):
    for n in range(1, 5):
        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)
        if case is not None:
            return case
    return None
''', 'test-7')

# ---- l16 equal_thirds
mutant('l16 equal_thirds', 'counts the first cut before checking the second', '''
def equal_thirds(xs):
    total = sum(xs)
    if total % 3 != 0: return 0
    third = total // 3
    ways, firsts, prefix = 0, 0, 0
    for j in range(len(xs) - 1):
        prefix += xs[j]
        if prefix == third: firsts += 1
        if prefix == 2 * third: ways += firsts
    return ways
''', 'test-2')
mutant('l16 equal_thirds', 'no divisibility test, third = total // 3', '''
def equal_thirds(xs):
    third = sum(xs) // 3
    ways, firsts, prefix = 0, 0, 0
    for j in range(len(xs) - 1):
        prefix += xs[j]
        if prefix == 2 * third: ways += firsts
        if prefix == third: firsts += 1
    return ways
''', 'test-5')
mutant('l16 equal_thirds', 'stops once the prefix passes 2S/3 (assumes prefixes only rise)', '''
def equal_thirds(xs):
    total = sum(xs)
    if total % 3 != 0: return 0
    third = total // 3
    ways, firsts, prefix = 0, 0, 0
    for j in range(len(xs) - 1):
        prefix += xs[j]
        if prefix > 2 * third: break
        if prefix == 2 * third: ways += firsts
        if prefix == third: firsts += 1
    return ways
''', 'test-6')
mutant('l16 equal_thirds', 'the double loop over cuts', '''
def equal_thirds(xs):
    n = len(xs); P = [0]
    for x in xs: P.append(P[-1] + x)
    ways = 0
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if P[i] == P[j] - P[i] == P[n] - P[j]:
                ways += 1
    return ways
''', 'test-8')

# ---- l16 mistakes_summary
mutant('l16 mistakes_summary', 'max() of an empty log', '''
def mistakes_summary(log):
    counts = {}
    for problem, category in log:
        counts[category] = counts.get(category, 0) + 1
    top = max(counts.values())
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
''', 'test-2')
mutant('l16 mistakes_summary', 'sorts names without regard to case', '''
def mistakes_summary(log):
    counts = {}
    for problem, category in log:
        counts[category] = counts.get(category, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))
''', 'test-6')
mutant('l16 mistakes_summary', 'sorts by name only', '''
def mistakes_summary(log):
    counts = {}
    for problem, category in log:
        counts[category] = counts.get(category, 0) + 1
    return sorted(counts.items())
''', 'test-7')
# test-4 names the missing alphabetical tie-break; test 1, the lesson's own log, already has a tie at 2
for label, body in [('sorts by count only (ties in order of first appearance)', 'sorted(counts.items(), key=lambda kv: -kv[1])'),
                    ('Counter.most_common', '__import__("collections").Counter(c for _, c in log).most_common()'),
                    ('sorts (count, name) downwards', 'sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)')]:
    mutant('l16 mistakes_summary', label + ' lands on test-1 (fix pass: line moved there)', '''
def mistakes_summary(log):
    counts = {}
    for problem, category in log:
        counts[category] = counts.get(category, 0) + 1
    return %s
''' % body, 'test-1', finding=6)

# ---- hw4 desks_after_cut
BFS = '''
from collections import deque
def desks_after_cut(n, links, cut):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(links):
        if %s:
            adj[a].append(b); adj[b].append(a)
    seen = [False] * n; groups = 0
    for s in %s:
        if seen[s]: continue
        groups += 1; seen[s] = True; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True; q.append(v)
    return groups
'''
mutant('hw4 desks_after_cut', 'removes every copy of the cut link', BFS % ('(a, b) != links[cut]', 'range(n)'), 'test-4')
# test-5 names isolated desks; example 2 (test 2) already has one, desk 3
mutant('hw4 desks_after_cut', 'starts only from desks that still have a link, lands on test-2 (fix pass: line moved there)', BFS % ('i != cut', '[s for s in range(n) if adj[s]]'), 'test-2', finding=7)
mutant('hw4 desks_after_cut', 'starts only from desks named in some link, lands on test-2 (fix pass: line moved there)', BFS % ('i != cut', 'sorted({x for ab in links for x in ab})'), 'test-2', finding=7)
mutant('hw4 desks_after_cut', 'recursive DFS (3,000 frames on the page)', '''
def desks_after_cut(n, links, cut):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(links):
        if i != cut:
            adj[a].append(b); adj[b].append(a)
    seen = [False] * n
    def dfs(u):
        seen[u] = True
        for v in adj[u]:
            if not seen[v]: dfs(v)
    groups = 0
    for s in range(n):
        if not seen[s]:
            groups += 1; dfs(s)
    return groups
''', 'test-7')

# ---- hw4 max_profit_k
mutant('hw4 max_profit_k', 'arrays of length k, answer read at k - 1 (k = 0 crashes)', '''
def max_profit_k(prices, k):
    buy = [float("-inf")] * k; sell = [0] * k
    for p in prices:
        for j in range(k):
            buy[j] = max(buy[j], (sell[j - 1] if j else 0) - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k - 1]
''', 'test-3')
mutant('hw4 max_profit_k', 'forces exactly k trades, each sold on a later day', '''
def max_profit_k(prices, k):
    NEG = float("-inf")
    buy = [NEG] * (k + 1); sell = [0] + [NEG] * k
    for p in prices:
        for j in range(k, 0, -1):
            sell[j] = max(sell[j], buy[j] + p)
            buy[j] = max(buy[j], sell[j - 1] - p)
    return sell[k]
''', 'test-4')
# test-6 names no mistake; it states the test's arithmetic, checked here (no simple slip was found that stops there first)
ck('B hw4 max_profit_k: test 6, ten trades allowed, three rises help: 2 + 3 + 4 = 9', (3 - 1) + (5 - 2) + (8 - 4) == 9)
mutant('hw4 max_profit_k', 'every pair of days for each trade, O(n^2 k)', '''
def max_profit_k(prices, k):
    n = len(prices)
    if n < 2 or k == 0: return 0
    prev = [0] * n
    for _ in range(k):
        cur = [0] * n
        for j in range(1, n):
            best = cur[j - 1]
            for i in range(j):
                best = max(best, (prev[i - 1] if i else 0) + prices[j] - prices[i])
            cur[j] = best
        prev = cur
    return prev[-1]
''', 'test-8')

# ---- hw4 widest_gap
GAP = '''
def widest_gap(levels, m):
    xs = %s
    def fits(gap):
        placed, last = 1, xs[0]
        for x in xs[1:]:
            if x - last >= gap:
                placed += 1; last = x
        return placed >= m
    %s
'''
BS = '''lo, hi = %d, xs[-1] - xs[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fits(mid): lo = mid
        else: hi = mid - 1
    return lo'''
mutant('hw4 widest_gap', 'search starts at distance 1', GAP % ('sorted(levels)', BS % 1), 'test-4')
# test-5 says "Test 5 is unsorted. Sort the levels": the example itself (test 1) is unsorted
mutant('hw4 widest_gap', 'no sort, lands on test-1 (fix pass: line moved there)', GAP % ('list(levels)', BS % 0), 'test-1', finding=8)
mutant('hw4 widest_gap', 'tries every distance upwards', GAP % ('sorted(levels)', '''d = 0
    while fits(d + 1): d += 1
    return d'''), 'test-8')

# ---------------------------------------------------------------- C. numbers and arguments
# ---- l13
ex = [3, 5, 4, 6, 2]
ck('C l13 A example 3 5 4 6 2 has 2 peaks', sum(1 for i in range(1, 4) if ex[i] > ex[i - 1] and ex[i] > ex[i + 1]) == 2)
ck('C l13 Sam: second wrong answer 13 minutes after the first, D 52 minutes, A 7', (51 - 38, 52 - 0, 59 - 52) == (13, 52, 7))
rows = L13['screens'][8]['widget']['rows']
cols = [sum(int(r[c]) for r in rows[:4]) for c in (1, 2, 3)]
ck('C l13 Alex log totals 16, 27, 17 and 60', cols == [16, 27, 17] and sum(cols) == 60 and [rows[4][c]['answer'] for c in (1, 2, 3)] == cols, cols)
ck('C l13 Alex per problem: A 9, B 17, C 27 (12 debugging), D 7, as the homework model says', [sum(int(x) for x in r[1:4]) for r in rows[:4]] == [9, 17, 27, 7] and int(rows[2][3]) == 12)
ck('C l13 B: a restart at every left end reads about n^2 / 2 = 2e10 trades at n = 200,000', 200000 * 200001 // 2 == 20000100000)
g = {}
exec(L13['screens'][5]['widget']['prelude'] + SOL_C, g)
w40 = g['_weights'](40, 32, 100)
ck('C l13 C test 10: 40 orders, total 1,807, heaviest 99, answer 909', (len(w40), sum(w40), max(w40), g['min_capacity'](w40, 2)) == (40, 1807, 99, 909), (sum(w40), max(w40)))
ck('C l13 C test 10: the search makes 11 can_ship calls, a scan upwards from 99 makes 811', g['checks_used'](w40, 2)[1] == 11 and 909 - 99 + 1 == 811, g['checks_used'](w40, 2))
w5 = g['_weights'](100000, 31)
ck('C l13 C test 11: about 30 checks by search, about a million by a scan', g['checks_used'](w5, 500)[1] in range(27, 32) and 1002823 - max(w5) > 990000, (g['checks_used'](w5, 500)[1], max(w5)))
ck('C l13 quiz: 2^30 = 1,073,741,824 > 1e9; 30 checks of 1e5 steps is 3e6', 2 ** 30 == 1073741824 and 30 * 10 ** 5 == 3 * 10 ** 6)
ck('C l13 summary formula: log2(total - heaviest) is 30 at the limits, 11 on test 10', math.ceil(math.log2(10 ** 9 - 10 ** 4)) == 30 and math.ceil(math.log2(1807 - 99)) == 11)
gd = {}
exec(L13['screens'][6]['widget']['solution'], gd)
EXG = ['..#.>', '.#>..', '.#.#.', '...v.']
ck('C l13 D example: 11 with arrows, 7 ignoring them; the v in the bottom row points off the grid', gd['grid_moves'](EXG) == 11 and gd['grid_moves']([r.replace('>', '.').replace('v', '.') for r in EXG]) == 7 and EXG[3][3] == 'v')
ck('C l13 D quiz: .> over v. is unreachable (-1)', gd['grid_moves'](['.>', 'v.']) == -1)
ck('C l13 transfer: 4 minutes is about a sixth of 75 / 3 = 25', abs(4 / 25 - 1 / 6) < 0.01)
ck('C l13 review r4-pattern: 2e5 redemptions of 1e9 is 2e14 limits', 2 * 10 ** 5 * 10 ** 9 == 2 * 10 ** 14)


# ---- l14: the decay rule (our rule: v/250 a minute, 50 a rejection, floor 0.3 v)
def sc(v, minute, wrong=0):
    return max(0.3 * v, v - v / 250 * minute - 50 * wrong)


PROBS = {'A': (500, 10), 'B': (1000, 20), 'C': (1500, 35), 'D': (2000, 50)}


def total(order, limit=120, probs=PROBS):
    clock, out = 0, []
    for p in order:
        v, t = probs[p]
        clock += t
        out.append(sc(v, clock) if clock <= limit else 0)
    return sum(out), out


ck('C l14 A B C D scores 480, 880, 1110, 1080 = 3,550', total('ABCD') == (3550, [480, 880, 1110, 1080]), total('ABCD'))
ck('C l14 D C B A scores 1600, 990, 580, 270 = 3,440', total('DCBA') == (3440, [1600, 990, 580, 270]), total('DCBA'))
ck('C l14 C A B D scores 1290, 410, 740, 1080 = 3,520', total('CABD') == (3520, [1290, 410, 740, 1080]), total('CABD'))
ck('C l14 hardest first: D gains 520, the other three lose 630', 1600 - 1080 == 520 and (480 - 270) + (880 - 580) + (1110 - 990) == 630)
allp = {''.join(o): total(o)[0] for o in itertools.permutations('ABCD')}
ck('C l14 3,550 is the best of all 24 orders, reached by ABCD and BACD only (the `same` pair)', max(allp.values()) == 3550 and sorted(k for k, v in allp.items() if v == 3550) == ['ABCD', 'BACD'], allp)
ck('C l14 rates 50, 50, 42.857, 40', [round(v / t, 3) for v, t in PROBS.values()] == [50, 50, 42.857, 40])
ck('C l14 no floor binds in any of the 24 orders at 120 minutes', all(sc(v, 115) > 0.3 * v for v, _ in PROBS.values()))
# the exchange argument: for neighbours i then j against j then i, the change in points lost is (v_j t_i - v_i t_j)/250,
# whatever the start time, while no floor binds and both finish in time
rng = random.Random(4)
okx = True
for _ in range(20000):
    vi, vj = rng.choice([500, 750, 1000, 1250, 1500, 2000]), rng.choice([500, 750, 1000, 1250, 1500, 2000])
    ti, tj, s = rng.randint(1, 30), rng.randint(1, 30), rng.randint(0, 40)
    lost_ij = vi / 250 * (s + ti) + vj / 250 * (s + ti + tj)
    lost_ji = vj / 250 * (s + tj) + vi / 250 * (s + tj + ti)
    okx &= abs((lost_ij - lost_ji) - (vj * ti - vi * tj) / 250) < 1e-9
    okx &= ((lost_ij < lost_ji) == (vi / ti > vj / tj)) or abs(vi / ti - vj / tj) < 1e-12
ck('C l14 exchange formula and its sign rule hold on 20,000 random neighbour pairs', okx)
# and the rule it proves: with no floor and no deadline, sorting by v/t is optimal (brute force, 2,000 random rounds of 5)
oks = True
for _ in range(2000):
    ps = [(rng.choice([500, 1000, 1500, 2000, 2500]), rng.randint(1, 12)) for _ in range(5)]
    best = min(sum(v / 250 * c for (v, _), c in zip(o, itertools.accumulate(t for _, t in o))) for o in itertools.permutations(ps))
    o = sorted(ps, key=lambda p: -p[0] / p[1])
    oks &= abs(sum(v / 250 * c for (v, _), c in zip(o, itertools.accumulate(t for _, t in o))) - best) < 1e-9
ck('C l14 points-per-minute order loses the fewest points in 2,000 random rounds (no floor, no deadline)', oks)
ck('C l14 C then D beats D then C by 20: 3,550 against 3,530', total('ABCD')[0] - total('ABDC')[0] == 20 and (2000 * 35 - 1500 * 50) / 250 == -20)
ck('C l14 B at minute 35 with one rejection: 810; slips 860, 760; floor 300', (sc(1000, 35, 1), 1000 - 140, 1000 - 140 - 100, 0.3 * 1000) == (810, 860, 760, 300))
ck('C l14 test lines: 110 under the floor 150; 300 exactly at minute 175; 100 under 450', (500 - 240 - 150, 1000 - 4 * 175, 1500 - 6 * 200 - 200, 0.3 * 1500) == (110, 300, 100, 450))
ck('C l14 ICPC table: 12 + (41 + 20) + (95 + 40) = 208', 12 + 61 + 135 == 208)
ck('C l14 ICPC quiz: X 195, Y 185, Z 400 with four solves', (15 + 50 + 90 + 40, 20 + 45 + 100 + 20, 60 + 70 + 80 + 190) == (195, 185, 400))
ck('C l14 60 minutes: B then C 2,090, A then B 1,360, no three problems fit', total('BCAD', 60)[0] == 2090 and total('ABCD', 60)[0] == 1360 and 10 + 20 + 35 > 60)
ck('C l14 60 minutes: 2,090 is the best of the 24 orders', max(total(o, 60)[0] for o in itertools.permutations('ABCD')) == 2090)
PQ = {'P': (750, 25), 'Q': (1250, 50)}
ck('C l14 quiz q-rate: P 30 a minute, Q 25; P then Q 1,550 beats Q then P 1,525', (750 / 25, 1250 / 50, total('PQ', 120, PQ)[0], total('QP', 120, PQ)[0]) == (30, 25, 1550, 1525))
ck('C l14 quiz q-floor: 1000 - 720 - 50 = 230, floored to 300; 280 without the rejection', (1000 - 720 - 50, sc(1000, 180, 1), 1000 - 720) == (230, 300, 280))
ck('C l14 scoreboard: 702 / 96 is about seven', 7 <= 702 / 96 < 7.5)
ck('C l14 desk: 600, 480 and 100 pounds a minute; quote and hedge fill the half hour', (3000 / 5, 12000 / 25, 2000 / 20, 5 + 25) == (600, 480, 100, 30))


# the D or E split curve
def E(x):
    return 1000 * (1 - math.exp(-x / 50)) + 800 * (1 - math.exp(-(60 - x) / 15))


xs = [i / 1000 for i in range(60001)]
xbest = max(xs, key=E)
ck('C l14 split curve: top at x = 34.84, 1,152.3 points; all D 699, all E 785; start point 952.73', abs(xbest - 34.84) < 0.01 and abs(E(xbest) - 1152.3) < 0.05 and round(E(60)) == 699 and round(E(0)) == 785 and abs(E(10) - 952.7300522442163) < 1e-9, (xbest, E(xbest)))
ck('C l14 split curve: 20 e^(-x/50) = (160/3) e^(-(60-x)/15) at the top', abs(20 * math.exp(-xbest / 50) - 160 / 3 * math.exp(-(60 - xbest) / 15)) < 0.01)

# the same model with the cap used as a cap (leave D for E the minute D is solved): V(x) is the expected score, and its
# top is where 20 = (160/3) e^(-(60-x)/15), x = 60 - 15 ln(8/3) = 45.3, not 34.84 (finding 9)
def V(x, steps=6000):
    h = x / steps
    acc = sum(math.exp(-(k + 0.5) * h / 50) / 50 * (1000 + 800 * (1 - math.exp(-(60 - (k + 0.5) * h) / 15))) for k in range(steps)) * h
    return acc + math.exp(-x / 50) * 800 * (1 - math.exp(-(60 - x) / 15))


vbest = max((i / 100 for i in range(6001)), key=lambda x: V(x, 600))
ck('C l14 split curve, stop-when-solved version: best cap 45.3 minutes, about 1,229 points', abs(vbest - (60 - 15 * math.log(8 / 3))) < 0.02 and abs(vbest - 45.29) < 0.02 and round(V(vbest)) == 1229, (vbest, V(vbest)))
ck('C l14 split curve, stop-when-solved version: a cap of 35 scores about 1,202, above the fixed split\'s 1,152', round(V(34.84)) == 1202 and V(34.84) > E(34.84), V(34.84))
rs = random.Random(9)


def sim(cap, n=200000):
    tot = 0
    for _ in range(n):
        d = rs.expovariate(1 / 50)
        t = min(d, cap)
        tot += (1000 if d <= cap else 0) + (800 if rs.expovariate(1 / 15) <= 60 - t else 0)
    return tot / n


s35, s45 = sim(34.84), sim(45.29)
ck('C l14 split curve, Monte Carlo of the stop-when-solved policy (200,000 rounds each): 1,202 at 35, 1,229 at 45', abs(s35 - V(34.84)) < 6 and abs(s45 - V(45.29)) < 6, (s35, s45))

# ---- l15
buggy = lambda xs, x: next((i for i in range(len(xs) - 2, -1, -1) if xs[i] == x), -1)
good = lambda xs, x: next((i for i in range(len(xs) - 1, -1, -1) if xs[i] == x), -1)
HAND = [([5], 5), ([3, 3, 3], 3), ([10 ** 9, 10 ** 9, 1], 10 ** 9), ([4, 7], 9)]
ck('C l15 hand cases: expected 0, 2, 1, -1; the submission gives -1, 1, 1, -1; two differ', [good(*h) for h in HAND] == [0, 2, 1, -1] and [buggy(*h) for h in HAND] == [-1, 1, 1, -1])
ck('C l15 the example 4 7 7 1 hides the bug', buggy([4, 7, 7, 1], 7) == good([4, 7, 7, 1], 7) == 2)
ck('C l15 test 7 of fix 2: 1,500 values make 1,124,250 pairs', 1500 * 1499 // 2 == 1124250)
ck('C l15 inversions of 2 1 2 1 is 3; of 3 2 1 is 3, with 2 between neighbours', sum(1 for i in range(4) for j in range(i + 1, 4) if [2, 1, 2, 1][i] > [2, 1, 2, 1][j]) == 3)
ck('C l15 quiz: 2e5 values of 1e9 sum to 2e14 > 2^31 - 1 = 2,147,483,647; long long to 9.2e18', 2 * 10 ** 5 * 10 ** 9 == 2 * 10 ** 14 > 2 ** 31 - 1 == 2147483647 and abs((2 ** 63 - 1) / 9.2e18 - 1) < 0.01)
# wide values almost never tie: chance that a draw of 8 values from 1..1e6 holds a tie, times the 1,600 draws of one call
p_tie = 1 - math.prod((10 ** 6 - i) / 10 ** 6 for i in range(8))
ck('C l15 values to 1e6: under 5% chance that 1,600 draws of at most 8 values hold any tie at all', 1600 * p_tie < 0.05, 1600 * p_tie)
# the smallest input that can expose the neighbours-only count has three values (exhaustive over 1..3)
gp = {}
exec(L15['screens'][9]['widget']['prelude'], gp)
ck('C l15 neighbours-only count: right on every list of length 1 or 2, wrong on some of length 3',
   all(gp['fast_adjacent'](list(c)) == gp['brute_inv'](list(c)) for n in (1, 2) for c in itertools.product((1, 2, 3), repeat=n))
   and any(gp['fast_adjacent'](list(c)) != gp['brute_inv'](list(c)) for c in itertools.product((1, 2, 3), repeat=3)))
ck('C l15 merge-sort count equals the brute force on every list of length up to 7 over 1..3',
   all(gp['fast_merge'](list(c)) == gp['brute_inv'](list(c)) for n in range(8) for c in itertools.product((1, 2, 3), repeat=n)))

# ---- l16
ck('C l16 C(199999, 2) = 19,999,700,001; C(4, 2) = 6; C(3, 2) = 3; C(5, 2) = 10', (math.comb(199999, 2), math.comb(4, 2), math.comb(3, 2), math.comb(5, 2)) == (19999700001, 6, 3, 10))
ck('C l16 the count is about nine times 2^31 - 1 and is exact in a double', 9 < 19999700001 / (2 ** 31 - 1) < 9.5 and float(19999700001) == 19999700001 < 2 ** 53)
gt = {}
exec(L16['screens'][3]['widget']['solution'], gt)


def thirds_brute(a):
    n = len(a)
    return sum(1 for i in range(1, n - 1) for j in range(i + 1, n) if sum(a[:i]) == sum(a[i:j]) == sum(a[j:]))


okt = all(gt['equal_thirds'](list(c)) == thirds_brute(list(c)) for n in range(1, 8) for c in itertools.product((-1, 0, 1, 2), repeat=n))
ck('C l16 equal_thirds equals the cut-by-cut brute force on every list of length up to 7 over -1..2', okt)
cats = [r[1] for r in L16['screens'][4]['canvas']['params']['rows']]
ck('C l16 log counts 3, 2, 2, 1 of 8', [cats.count(c) for c in ('forgot n = 1', 'misread a constraint', 'greedy without proof', 'overflow')] == [3, 2, 2, 1] and len(cats) == 8)
ck('C l16 ranges: 1200 + 300 = 1500; E 700 and F 1,200 above; 2000 is 750 above 1,250; 1800 - 1410 = 390', (1200 + 300, 1900 - 1200, 2400 - 1200, 2000 - 1250, 1800 - 1410) == (1500, 700, 1200, 750, 390))

# ---- review-4 and homework-4
ck('C r4 debugging share 18 / 60 = 0.3; coding 0.5; debugging over coding 0.6', (18 / 60, 30 / 60, 18 / 30) == (0.3, 0.5, 0.6))
ck('C r4 decay: 1500 - 288 - 100 = 1,112; slips 1,212 and 1,162; floor 450', (sc(1500, 48, 2), 1500 - 288, 1500 - 288 - 50, 0.3 * 1500) == (1112, 1212, 1162, 450))
RQ = {'P': (1000, 40), 'Q': (500, 15)}
ck('C r4 swap: Q then P 1,250, P then Q 1,230; waits cost 60 and 80; rates 33.3 and 25', (total('QP', 120, RQ)[0], total('PQ', 120, RQ)[0], 15 * 4, 40 * 2, round(500 / 15, 1), 1000 / 40) == (1250, 1230, 60, 80, 33.3, 25))
ck('C r4 late: E at minute 115 scores 675; 20-minute slip 1,150; floor 375', (sc(1250, 115), 1250 - 5 * 20, 0.3 * 1250) == (675, 1150, 375))
ck('C r4 hand: the loop from index 1 gives 0 on [5], 4 on [2, 2, 2], 0 on []', (sum([5][1:]), sum([2, 2, 2][1:]), sum([][1:])) == (0, 4, 0))
ck('C r4 upsolve: 1350 + 300 = 1650; 1900 and 2300 are 550 and 950 above', (1350 + 300, 1900 - 1350, 2300 - 1350) == (1650, 550, 950))
ck('C hw4 penalty: 8 + 27 + 64 + 110 = 209, + 60 = 269; with E 349', (8 + 27 + 64 + 110, 209 + 60, 269 + 80) == (209, 269, 349))
ck('C hw4 k trades: O(n^2 k) is 2e9 and O(nk) is 2e5 at n = 1e4, k = 20', (10 ** 8 * 20, 10 ** 4 * 20) == (2 * 10 ** 9, 2 * 10 ** 5))
gk = {}
exec(H4['items'][1]['widget']['solution'], gk)


def kbrute(p, k):
    n = len(p)
    best = 0
    def go(i, left, cash):
        nonlocal best
        best = max(best, cash)
        if left == 0: return
        for b in range(i, n):
            for s in range(b + 1, n):
                if p[s] > p[b]: go(s, left - 1, cash + p[s] - p[b])
    go(0, k, 0)
    return best


r5 = random.Random(5)
ck('C hw4 max_profit_k equals a brute force over trades on 400 random price lists', all(gk['max_profit_k'](p, k) == kbrute(p, k) for p, k in (([r5.randint(1, 9) for _ in range(r5.randint(1, 7))], r5.randint(0, 4)) for _ in range(400))))
gg = {}
exec(H4['items'][2]['widget']['solution'], gg)
r6 = random.Random(6)


def gbrute(xs, m):
    return max(min(b - a for a, b in zip(c, c[1:])) for c in itertools.combinations(sorted(xs), m))


ck('C hw4 widest_gap equals choosing every set of m levels on 400 random lists', all(gg['widest_gap'](xs, m) == gbrute(xs, m) for xs, m in ((lambda xs: (xs, r6.randint(2, len(xs))))([r6.randint(1, 12) for _ in range(r6.randint(2, 7))]) for _ in range(400))))
ck('C hw4 desks: the chain cut at link n // 2 leaves a run of 100,001 desks, 100,000 calls deep', 200000 // 2 + 1 == 100001)

# ---------------------------------------------------------------- D. optional: the solutions in Pyodide
if '--pyodide' in sys.argv:
    pkgs = os.path.abspath(sys.argv[sys.argv.index('--pyodide') + 1])
    jobs = [{'name': n, 'prelude': it['widget'].get('prelude', ''), 'code': it['widget']['solution'], 'tests': it['widget']['tests']} for n, (it, _) in WIDGETS.items()]
    drv = r'''
import json, math, sys, time
sys.setrecursionlimit(3000)
def _same(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    return bool(x == y)
def _close(x, y):
    try: return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception: return x == y
out = []
for job in json.loads(JOBS):
    g = {'__name__': '__main__'}
    exec(job['prelude'], g); exec(job['code'], g)
    res = []
    for t in job['tests']:
        t0 = time.time()
        if t.get('setup'): exec(t['setup'], g)
        a = eval(t['call'], g); e = eval(str(t['expect']), g)
        res.append([bool(_close(a, e) if t.get('compare') == 'isclose' else _same(a, e)), round(time.time() - t0, 3)])
    out.append([job['name'], res])
# the claim in l15 screens[7]: a million nested frames run once the limit is raised
sys.setrecursionlimit(10**6 + 100)
def deep(n): return 0 if n == 0 else 1 + deep(n - 1)
out.append(['million frames', [[deep(10**6) == 10**6, 0]]])
sys.setrecursionlimit(3000)
try:
    deep(3500); out.append(['limit 3000', [[False, 0]]])
except RecursionError:
    out.append(['limit 3000', [[True, 0]]])
out.append(['wasm32', [[sys.maxsize == 2**31 - 1 and sys.version_info[:2] == (3, 12), 0]]])
RESULT = json.dumps(out)
'''
    mjs = '''
import path from 'node:path'; import fs from 'node:fs'; import { pathToFileURL } from 'node:url';
const dir = path.join(%s, 'pyodide-0.27.7', 'package');
const { loadPyodide } = await import(pathToFileURL(path.join(dir, 'pyodide.mjs')).href);
const py = await loadPyodide({ indexURL: dir + '/' });
py.globals.set('JOBS', fs.readFileSync(%s, 'utf8'));
py.runPython(fs.readFileSync(%s, 'utf8'));
console.log('RESULT ' + py.globals.get('RESULT'));
'''
    with tempfile.TemporaryDirectory() as td:
        jf, df, mf = os.path.join(td, 'jobs.json'), os.path.join(td, 'drv.py'), os.path.join(td, 'run.mjs')
        open(jf, 'w').write(json.dumps(jobs)); open(df, 'w').write(drv)
        open(mf, 'w').write(mjs % (json.dumps(pkgs), json.dumps(jf), json.dumps(df)))
        p = subprocess.run(['node', mf], capture_output=True, text=True, timeout=900)
    line = next((l for l in p.stdout.splitlines() if l.startswith('RESULT ')), None)
    ck('D Pyodide run produced a result', line is not None, (p.stdout[-300:], p.stderr[-300:]))
    if line:
        worst = ('', 0.0)
        for name, res in json.loads(line[7:]):
            ck('D Pyodide: %s passes' % name, all(r[0] for r in res), res)
            ck('D Pyodide: %s every test under 5 s' % name, all(r[1] < 5 for r in res), max(r[1] for r in res))
            if max(r[1] for r in res) > worst[1]:
                worst = (name, max(r[1] for r in res))
        print('Pyodide: slowest solution test %.2f s (%s)' % (worst[1], worst[0]))

print('%d checks, %d failing' % (N[0], len(FAIL)))
for f in FAIL:
    print('  FAIL ' + f)
sys.exit(1 if FAIL else 0)
