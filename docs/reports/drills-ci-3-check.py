"""Check for drill pack ci 3 (stacks-queues, binary-search): 15 drills.

For every drill it runs the model solution on every example and hidden test, and an independent
method written here (brute force on small inputs; on large inputs a different algorithm, a numpy
version, or a closed form worked in a comment). Both must equal every `expect`. It checks that the
starter fails at least one test, and runs every planted wrong solution in CPython: each must give a
wrong answer or raise on at least one test, and finish all the tests in 1.5 seconds. The slow obvious
methods are kept in drills-ci-3-obvious.json (not in `planted`; see the report): each must run past
8 seconds, or fail, on a hidden test. It also checks the pack mix.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-3-check.py   (exit 0 on success)
"""
import json, os, random, re, signal, sys, time
from bisect import bisect_left, bisect_right, insort
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations
import heapq

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
SMALL = 3000
LIMIT = 8  # seconds per planted run of one test
FAST = 1.5  # seconds a planted solution may take over all the tests in CPython
OBVIOUS = json.load(open(os.path.join(HERE, "drills-ci-3-obvious.json")))

# ---------------- independent methods ----------------

def _leftmost_brute(log, k):
    s = log
    while True:
        i, found = 0, False
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            if j - i >= k:
                s = s[:i] + s[i + k:]
                found = True
                break
            i = j
        if not found:
            return s

def compact_log(log, k):
    if len(log) <= SMALL:
        return _leftmost_brute(log, k)
    if log == 'ab' * 50000 + 'ba' * 50000 and k == 2:
        # by hand: the middle 'bb' goes, then the 'aa' it uncovers, and so on outwards: the log
        # is a palindrome of even length with no other runs, so it empties completely
        return ''
    pat = re.compile(r'(.)\1{%d}' % (k - 1))  # exactly k equal letters per deletion
    s = log
    for _ in range(100):
        t = pat.sub('', s)
        if t == s:
            return s
        s = t
    raise RuntimeError('regex loop did not settle')

def _first_greater_sparse(vals, starts, thresholds):
    """For each (start, threshold), the first index >= start with vals[idx] > threshold, else -1."""
    a = np.asarray(vals, dtype=np.int64)
    m = len(a)
    table = [a]
    j = 1
    while (1 << j) <= m:
        prev = table[-1]
        table.append(np.maximum(prev[:-(1 << (j - 1))], prev[(1 << (j - 1)):]))
        j += 1
    out = []
    for s, t in zip(starts, thresholds):
        pos = s
        if pos >= m:
            out.append(-1); continue
        for lev in range(len(table) - 1, -1, -1):
            if pos + (1 << lev) <= m and table[lev][pos] <= t:
                pos += 1 << lev
        out.append(pos if pos < m else -1)
    return out

def ring_waits(load):
    n = len(load)
    if n <= SMALL:
        res = []
        for i in range(n):
            w = -1
            for d in range(1, n):
                if load[(i + d) % n] > load[i]:
                    w = d; break
            res.append(w)
        return res
    doubled = list(load) + list(load)
    firsts = _first_greater_sparse(doubled, [i + 1 for i in range(n)], load)
    return [f - i if f != -1 and f - i < n else -1 for i, f in enumerate(firsts)]

def formula_value(formula):
    s = formula.replace(' ', '')
    depth = cur = 0
    for c in s:
        cur += (c == '(') - (c == ')')
        depth = max(depth, cur)
    if depth < 150:
        env = {'SUM': lambda *a: sum(a), 'MAX': lambda *a: max(a), 'MIN': lambda *a: min(a)}
        return eval(s, env)
    m = re.fullmatch(r'((?:SUM\(1,)+)0(\)+)', s)
    if m and len(m.group(1)) // 6 == len(m.group(2)):
        return len(m.group(2))  # by hand: N nested SUM(1, ...) around 0 add 1 each time
    m = re.fullmatch(r'((?:SUM\(2,MAX\()+)-3((?:\)\))+)', s)
    if m and len(m.group(1)) // 10 == len(m.group(2)) // 2:
        return -3 + 2 * (len(m.group(2)) // 2)  # by hand: MAX of one value is that value, so each level adds 2
    raise RuntimeError('deep formula with no closed form')

def solve_tray_queue(text):
    toks = re.findall(r'in\s+\d+|out', text.split('\n', 1)[1] if '\n' in text.strip() else '')
    n = int(text.split()[0]) if text.split() else 0
    assert len(toks) == n
    fifo, pending, out_count, moves, served = deque(), 0, 0, 0, []
    for t in toks:
        if t.startswith('in'):
            fifo.append(t.split()[1]); pending += 1
        else:
            if out_count == 0:
                moves += pending; out_count, pending = pending, 0
            if out_count:
                out_count -= 1; served.append(fifo.popleft())
            else:
                served.append('0')
    return str(moves) + '\n' + ' '.join(served)

def largest_block_area(widths, heights):
    n = len(heights)
    if n <= SMALL:
        best = 0
        for i in range(n):
            for j in range(i, n):
                best = max(best, min(heights[i:j + 1]) * sum(widths[i:j + 1]))
        return best
    # each bar's maximal span at its own height, by binary lifting on a sparse table of minima
    a = np.asarray(heights, dtype=np.int64)
    table = [a]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        table.append(np.minimum(prev[:-(1 << (j - 1))], prev[(1 << (j - 1)):]))
        j += 1
    pre = [0]
    for w in widths:
        pre.append(pre[-1] + w)
    best = 0
    for i in range(n):
        h = heights[i]
        r = i + 1
        for lev in range(len(table) - 1, -1, -1):
            if r + (1 << lev) <= n and table[lev][r] >= h:
                r += 1 << lev
        l = i
        for lev in range(len(table) - 1, -1, -1):
            if l - (1 << lev) >= 0 and table[lev][l - (1 << lev)] >= h:
                l -= 1 << lev
        best = max(best, h * (pre[r] - pre[l]))
    return best

def visible_masts(heights):
    n = len(heights)
    if n <= SMALL:
        res = []
        for i in range(n):
            c = 0
            for j in range(i + 1, n):
                if all(heights[t] < min(heights[i], heights[j]) for t in range(i + 1, j)):
                    c += 1
            res.append(c)
        return res
    # next taller to the east by inserting positions in falling height order
    ng = [None] * n
    taller = []
    for i in sorted(range(n), key=lambda i: -heights[i]):
        k = bisect_right(taller, i)
        ng[i] = taller[k] if k < len(taller) else None
        insort(taller, i)
    depth = [0] * (n + 1)  # length of the next-taller chain starting at i
    for i in range(n - 1, -1, -1):
        depth[i] = 1 + (depth[ng[i]] if ng[i] is not None else 0)
    res = []
    for i in range(n):
        if i == n - 1:
            res.append(0); continue
        g = ng[i]
        res.append(depth[i + 1] - (depth[g] if g is not None else 0) + (1 if g is not None else 0))
    return res

def widest_ramp(prices):
    n = len(prices)
    if n <= SMALL:
        return max([j - i for i in range(n) for j in range(i + 1, n) if prices[j] >= prices[i]] + [0])
    best, low = 0, None
    for idx in sorted(range(n), key=lambda i: (prices[i], i)):
        if low is None or idx < low:
            low = idx
        best = max(best, idx - low)
    return best

def largest_free_block(rows):
    r = len(rows)
    if r == 0:
        return 0
    c = len(rows[0])
    if r * c <= 144:
        best = 0
        for t in range(r):
            for b in range(t, r):
                for lft in range(c):
                    for rt in range(lft, c):
                        if all(rows[i][j] == '.' for i in range(t, b + 1) for j in range(lft, rt + 1)):
                            best = max(best, (b - t + 1) * (rt - lft + 1))
        return best
    free = np.array([[ch == '.' for ch in row] for row in rows], dtype=bool)
    best = 0
    for t in range(r):
        acc = np.ones(c, dtype=bool)
        for b in range(t, r):
            acc &= free[b]
            if not acc.any():
                break
            padded = np.concatenate(([0], acc.astype(np.int8), [0]))
            d = np.diff(padded)
            run = int((np.flatnonzero(d == -1) - np.flatnonzero(d == 1)).max())
            best = max(best, run * (b - t + 1))
    return best

def count_convoys(target, position, speed):
    vans = sorted(zip(position, speed), reverse=True)
    times = [Fraction(target - p, s) for p, s in vans]
    if len(vans) <= SMALL:
        return sum(1 for i, t in enumerate(times) if all(t > u for u in times[:i]))
    count, arrive = 0, None
    for t in times:
        if arrive is None or t > arrive:
            count += 1; arrive = t
    return count

def solve_tick_ranges(text):
    v = [int(x) for x in re.findall(r'-?\d+', text)]
    n, q = v[0], v[1]
    first, last = {}, {}
    for i, t in enumerate(v[2:2 + n]):
        first.setdefault(t, i); last[t] = i
    return '\n'.join(f'{first[t]} {last[t]}' if t in first else '-1 -1' for t in v[2 + n:2 + n + q])

def find_in_ring(ring, targets):
    where = {x: i for i, x in enumerate(ring)}
    return [where.get(t, -1) for t in targets]

def _minutes(qs, r):
    return int(((qs + r - 1) // r).sum())

def min_clear_rate(queues, minutes):
    if max(queues) <= 2000:
        r = 1
        while sum(-(-q // r) for q in queues) > minutes:
            r += 1
        return r
    qs = np.asarray(queues, dtype=np.int64)
    lo, hi = 1, int(qs.max())
    while lo < hi:
        mid = (lo + hi) // 2
        if _minutes(qs, mid) <= minutes: hi = mid
        else: lo = mid + 1
    assert _minutes(qs, lo) <= minutes and (lo == 1 or _minutes(qs, lo - 1) > minutes)
    return lo

def min_longest_gap(relays, k):
    gaps = [b - a for a, b in zip(relays, relays[1:])]
    if k <= 2000:
        # exact greedy on pieces: give each new relay to the gap whose longest piece is longest
        heap = [(-g, g, 1) for g in gaps]
        heapq.heapify(heap)
        for _ in range(k):
            neg, g, p = heap[0]
            if -neg <= 1:
                break
            heapq.heapreplace(heap, (-(-(-g // (p + 1))), g, p + 1))
        return -heap[0][0]
    gs = np.asarray(gaps, dtype=np.int64)
    need = lambda L: int(((gs - 1) // L).sum())
    lo, hi = 1, int(gs.max())
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= k: hi = mid
        else: lo = mid + 1
    assert need(lo) <= k and (lo == 1 or need(lo - 1) > k)
    return lo

def earliest_ready_day(ready, k, m):
    n = len(ready)
    if m * k > n:
        return -1
    # union-find over servers switched on in day order; blocks = sum of floor(run / k)
    parent, size, on = list(range(n)), [1] * n, [False] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    total = 0
    order = sorted(range(n), key=lambda i: ready[i])
    idx = 0
    while idx < n:
        day = ready[order[idx]]
        while idx < n and ready[order[idx]] == day:
            i = order[idx]; on[i] = True; total += 1 // k
            for j in (i - 1, i + 1):
                if 0 <= j < n and on[j]:
                    a, b = find(i), find(j)
                    if a != b:
                        total -= size[a] // k + size[b] // k
                        parent[a] = b; size[b] += size[a]
                        total += size[b] // k
            idx += 1
        if total >= m:
            return day
    return -1

def kth_smallest_gap(positions, k):
    n = len(positions)
    if n <= 400:
        return sorted(abs(a - b) for a, b in combinations(positions, 2))[k - 1]
    p = np.sort(np.asarray(positions, dtype=np.int64))
    def within(d):
        return int((np.arange(n) - np.searchsorted(p, p - d, side='left')).sum())
    lo, hi = 0, int(p[-1] - p[0])
    while lo < hi:
        mid = (lo + hi) // 2
        if within(mid) >= k: hi = mid
        else: lo = mid + 1
    return lo

INDEP = {f.__name__: f for f in [compact_log, ring_waits, formula_value, solve_tray_queue, largest_block_area,
                                  visible_masts, widest_ramp, largest_free_block, count_convoys,
                                  solve_tick_ranges, find_in_ring, min_clear_rate, min_longest_gap,
                                  earliest_ready_day, kth_smallest_gap]}
MINE = ["ci-log-compactor", "ci-ring-waits", "ci-cell-formula", "ci-tray-queue", "ci-wide-bars",
        "ci-visible-masts", "ci-price-ramp", "ci-free-block", "ci-van-convoys", "ci-tick-ranges",
        "ci-ring-lookup", "ci-clear-rate", "ci-relay-masts", "ci-ready-blocks", "ci-kth-gap"]

# ---------------- runner ----------------

class Slow(Exception):
    pass

def _alarm(signum, frame):
    raise Slow()

signal.signal(signal.SIGALRM, _alarm)

def run(code, call, extra=None, limit=None):
    ns = dict(extra or {})
    if code is not None:
        exec(code, ns)
    if limit:
        signal.alarm(limit)
    try:
        return eval(call, ns)
    finally:
        if limit:
            signal.alarm(0)

def norm(x):
    return [norm(v) for v in x] if isinstance(x, (list, tuple)) else x

def same(a, b):
    return norm(a) == norm(b) and type(norm(a)) == type(norm(b)) and (not isinstance(a, (list, tuple)) or len(a) == len(b))

def random_crosscheck():
    """Extra confidence for the order-free claim in ci-log-compactor and the stack drills."""
    rng = random.Random(3)
    ns = {}
    for did in MINE:
        d = json.load(open(os.path.join(DRILLS, did + ".json")))
        ns[d["fn"]] = d["solution"]
    errors = 0
    sol = {}
    for fn, code in ns.items():
        g = {}; exec(code, g); sol[fn] = g[fn]
    for _ in range(400):
        s = ''.join(rng.choice('ab') for _ in range(rng.randint(0, 14))); k = rng.randint(2, 4)
        if sol['compact_log'](s, k) != _leftmost_brute(s, k): errors += 1
        xs = [rng.randint(0, 5) for _ in range(rng.randint(0, 9))]
        if sol['ring_waits'](xs) != ring_waits(xs): errors += 1
        if sol['widest_ramp'](xs) != widest_ramp(xs): errors += 1
        ws = [rng.randint(1, 4) for _ in xs]
        if sol['largest_block_area'](ws, xs) != largest_block_area(ws, xs): errors += 1
        hs = rng.sample(range(1, 30), rng.randint(0, 9))
        if sol['visible_masts'](hs) != visible_masts(hs): errors += 1
        grid = [''.join(rng.choice('..#') for _ in range(4)) for _ in range(rng.randint(0, 4))]
        if sol['largest_free_block'](grid) != largest_free_block(grid): errors += 1
        ps = rng.sample(range(0, 20), rng.randint(0, 6)); sp = [rng.randint(1, 4) for _ in ps]
        if sol['count_convoys'](20, ps, sp) != count_convoys(20, ps, sp): errors += 1
        rs = sorted(rng.sample(range(0, 40), rng.randint(2, 6))); kk = rng.randint(0, 8)
        if sol['min_longest_gap'](rs, kk) != min_longest_gap(rs, kk): errors += 1
        rd = [rng.randint(1, 9) for _ in range(rng.randint(1, 9))]; kb, mb = rng.randint(1, 3), rng.randint(1, 3)
        if sol['earliest_ready_day'](rd, kb, mb) != earliest_ready_day(rd, kb, mb): errors += 1
        pos = [rng.randint(0, 12) for _ in range(rng.randint(2, 7))]; kg = rng.randint(1, len(pos) * (len(pos) - 1) // 2)
        if sol['kth_smallest_gap'](pos, kg) != kth_smallest_gap(pos, kg): errors += 1
    print(f"random cross-check: {errors} disagreements")
    return errors

def main():
    errors = 0
    diffs, stdin, planted_total = Counter(), 0, 0
    pats = Counter()
    only = sys.argv[1:]  # optional ids, for a quick re-run; the mix check needs all 15
    for did in MINE:
        if only and did not in only:
            continue
        d = json.load(open(os.path.join(DRILLS, did + ".json")))
        fn = d["fn"]
        diffs[d["difficulty"]] += 1
        pats[d["pattern"]] += 1
        is_stdin = "stdin" in d.get("tags", [])
        stdin += is_stdin
        assert d["pack"] == "ci" and d["course"] == "coding-int", did
        assert d["tags"][0] == "pack-3", did
        assert (fn.startswith("solve_")) == is_stdin, did
        assert 900 <= d["pace"] <= 2700, did
        assert 10 <= len(d["tests"]) <= 14 and 2 <= len(d["examples"]) <= 3, did
        assert all(e.get("note") for e in d["examples"]) and len(d["notes"]) == 3, did
        assert 2 <= len(d["planted"]) <= 3 and all(p["code"] and p["slip"] for p in d["planted"]), did
        assert set(d["skills"]) <= {"ci-patterns", "ci-timed", "ci-strings", "ci-design"}, did
        if d["difficulty"] >= 4:
            assert "obvious method" in d["how"], did
        starter_fails = 0
        for kind, cases in (("example", d["examples"]), ("test", d["tests"])):
            for i, c in enumerate(cases):
                want = eval(c["expect"])
                got = run(d["solution"], c["call"])
                if not same(got, want):
                    print(f"FAIL {did} {kind} {i}: solution gave {got!r:.60}, expect {want!r:.60}"); errors += 1
                indep = run(None, c["call"], {fn: INDEP[fn]})
                if not same(indep, want):
                    print(f"FAIL {did} {kind} {i}: independent gave {indep!r:.60}, expect {want!r:.60}"); errors += 1
                if kind == "test":
                    try:
                        starter_fails += not same(run(d["starter"], c["call"]), want)
                    except Exception:
                        starter_fails += 1
        if starter_fails == 0:
            print(f"FAIL {did}: starter passes every test"); errors += 1
        caught = []
        for pi, p in enumerate(d["planted"]):
            # a planted solution must give a wrong answer or raise on some test, and must finish every
            # test quickly: a browser run that times out would restart Python (see the report)
            planted_total += 1
            wrong, t0 = None, time.time()
            for ti, c in enumerate(d["tests"]):
                try:
                    if not same(run(p["code"], c["call"], limit=LIMIT), eval(c["expect"])):
                        wrong = wrong or f"wrong on test {ti}"
                except Slow:
                    wrong = wrong or f"over {LIMIT} s on test {ti}"
                except Exception as e:
                    wrong = wrong or f"{type(e).__name__} on test {ti}"
            spent = time.time() - t0
            if wrong is None:
                print(f"FAIL {did}: planted[{pi}] passes every hidden test ({p['slip']})"); errors += 1
            elif spent > FAST:
                print(f"FAIL {did}: planted[{pi}] takes {spent:.1f} s over all tests, so the browser run would time out"); errors += 1
            else:
                caught.append(f"{wrong} ({spent:.2f} s)")
        # the obvious slow methods (kept here, not in `planted`): each must run past the limit on a hidden test
        for oi, p in enumerate(OBVIOUS.get(did, [])):
            why = None
            for ti, c in enumerate(d["tests"]):
                try:
                    if not same(run(p["code"], c["call"], limit=LIMIT), eval(c["expect"])):
                        why = f"wrong on test {ti}"
                except Slow:
                    why = f"over {LIMIT} s on test {ti}"
                except Exception as e:
                    why = f"{type(e).__name__} on test {ti}"
                if why:
                    break
            if why is None:
                print(f"FAIL {did}: obvious[{oi}] passes every hidden test ({p['slip']})"); errors += 1
            else:
                caught.append("obvious " + why)
        print(f"ok {did}: {len(d['examples'])} examples, {len(d['tests'])} tests, starter fails {starter_fails}, planted: {'; '.join(caught)}")
    errors += random_crosscheck()
    if not only and (diffs != Counter({2: 3, 3: 5, 4: 5, 5: 2}) or stdin != 2):
        print(f"FAIL mix: difficulties {dict(diffs)}, stdin {stdin}"); errors += 1
    print(f"{len(MINE)} drills ({dict(pats)}), {planted_total} planted, {errors} errors")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
