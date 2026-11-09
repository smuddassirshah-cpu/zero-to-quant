"""Extra checks behind the findings: brute force on small inputs, claim checks, and every proposed new test
computed twice (the model solution and the reader's own solution or a brute force).
Usage: extra_checks.py <drills_dir>. Exit 0 when every check behaves as the review says."""
import itertools, json, os, random, sys, time
sys.setrecursionlimit(10000)
DD = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
bad = 0


def model(i):
    ns = {}
    exec(json.load(open(os.path.join(DD, i + '.json')))['solution'], ns)
    return ns


def mine(mod):
    ns = {}
    exec(open(os.path.join(HERE, mod)).read(), ns)
    return ns


def check(label, cond):
    global bad
    print(('ok   ' if cond else 'FAIL ') + label)
    if not cond:
        bad += 1


MC, MD, MB = mine('mine_c.py'), mine('mine_d.py'), mine('mine_b3.py')
WD = {}
sys.argv = [sys.argv[0], 'x', 'x', DD]
exec(open(os.path.join(HERE, 'wrong_d.py')).read(), WD)
WC = {}
exec(open(os.path.join(HERE, 'wrong_c.py')).read(), WC)


def wrong(W, i, prefix):
    for lab, src in W['WRONG'][i]:
        if lab.startswith(prefix):
            ns = {}
            exec(src, ns)
            return ns
    raise KeyError(prefix)


R = random.Random(18)

# 1. dsa-shift-pay notes[1]: starting `one` and `two` at 0 never lets a third day slip through.
m = model('dsa-shift-pay')['solve_shift_pay']
w = wrong(WD, 'dsa-shift-pay', '1')['solve_shift_pay']
def brute_shift(p):
    best = 0
    for mask in range(1 << len(p)):
        if any((mask >> i) & 7 == 7 for i in range(len(p))):
            continue
        best = max(best, sum(x for i, x in enumerate(p) if mask >> i & 1))
    return best
agree = True
for n in range(0, 11):
    for _ in range(60):
        p = [R.randint(0, 9) for _ in range(n)]
        t = '%d\n%s\n' % (n, ' '.join(map(str, p)))
        b = brute_shift(p)
        if not (m(t) == w(t) == str(b)):
            agree = False
check('shift-pay: zero-start version equals model and brute force on 660 small cases (notes[1] reason is false)', agree)

# 2. dsa-kiosk-change: three-fives-first greedy passes every test; proposed test.
mk = model('dsa-kiosk-change')['first_short_change']
wk = wrong(WD, 'dsa-kiosk-change', '1')['first_short_change']
case = [5, 5, 5, 5, 10, 20, 10, 10]
check('kiosk: new test [5,5,5,5,10,20,10,10] -> -1 (model %s, mine %s), wrong greedy gives %s' % (mk(case), MD['first_short_change'](case), wk(case)),
      mk(case) == MD['first_short_change'](case) == -1 and wk(case) == 6)
# brute force of kiosk over every change choice
def brute_kiosk(notes):
    states = {(0, 0)}
    for i, x in enumerate(notes):
        nxt = set()
        for f, t in states:
            if x == 5: nxt.add((f + 1, t))
            elif x == 10:
                if f: nxt.add((f - 1, t + 1))
            else:
                if f and t: nxt.add((f - 1, t - 1))
                if f >= 3: nxt.add((f - 3, t))
        if not nxt:
            return i
        states = nxt
    return -1
ok = all(mk(q) == brute_kiosk(q) for q in (tuple(R.choice((5, 5, 10, 20)) for _ in range(R.randint(0, 12))) for _ in range(3000)))
check('kiosk: model equals the all-choices brute force on 3000 random queues', ok)
big = [5, 5, 5, 5, 10, 20, 10, 10] * 25000
check('kiosk: large test of the pattern x25000 -> -1 (model %s, mine %s), wrong %s' % (mk(big), MD['first_short_change'](big), wk(big)),
      mk(big) == MD['first_short_change'](big) == -1 and wk(big) == 6)

# 3. dsa-lift-buttons: floor-0 and greedy wrong solutions pass; proposed tests.
ml = model('dsa-lift-buttons')['solve_lift_buttons']
w0 = wrong(WD, 'dsa-lift-buttons', '1')['solve_lift_buttons']
wg = wrong(WD, 'dsa-lift-buttons', 'V greedy')['solve_lift_buttons']
t1 = '4 2 3 3 2\n'
check('lift: new test %r -> -1 (model %s, mine %s), floor-0 version gives %s' % (t1, ml(t1), MD['solve_lift_buttons'](t1), w0(t1)),
      ml(t1) == MD['solve_lift_buttons'](t1) == '-1' and w0(t1) != '-1')
found = None
for n in range(2, 13):
    for st in range(1, n + 1):
        for g in range(1, n + 1):
            for u in range(0, n + 1):
                for d in range(0, n + 1):
                    t = '%d %d %d %d %d\n' % (n, st, g, u, d)
                    if found is None and ml(t) != wg(t):
                        found = t
check('lift: the up-if-below greedy agrees with the model on every input with n <= 12, so it is not counted as a wrong solution', found is None)

# 4. dsa-print-queue: tie by arrival before id.
mp = model('dsa-print-queue')['solve_print_queue']
wp = wrong(WC, 'dsa-print-queue', '2')['solve_print_queue']
t3 = '3\n1 0 5\n9 1 2\n4 2 2\n'
check('print-queue: new test %r -> "1 9 4" (model %s, mine %s), id-tie version %s' % (t3, mp(t3), MC['solve_print_queue'](t3), wp(t3)),
      mp(t3) == MC['solve_print_queue'](t3) == '1 9 4' and wp(t3) == '1 4 9')

# 5. dsa-loop-depots: driving from every depot passes; proposed large test.
mL = model('dsa-loop-depots')['loop_start_depot']
f = [1] * 200000
b = [1] * 199998 + [2, 0]
t0 = time.time(); a1 = mL(f, b); dt = time.time() - t0
check('loop-depots: new test -> 199999 (model %s in %.2fs, mine %s)' % (a1, dt, MD['loop_start_depot'](f, b)), a1 == MD['loop_start_depot'](f, b) == 199999)
slow = wrong(WD, 'dsa-loop-depots', '3')['loop_start_depot']
f2 = [1] * 3000; b2 = [1] * 2998 + [2, 0]
t0 = time.time(); r2 = slow(f2, b2); dt2 = time.time() - t0
check('loop-depots: per-start drive costs n^2/2 on that shape (n=3000: %.2fs, answer %s), so about %.0fs at n=200000' % (dt2, r2, dt2 * (200000 / 3000) ** 2), r2 == 2999)
def brute_loop(fu, bu):
    n = len(fu)
    for s in range(n):
        t = 0
        for k in range(n):
            i = (s + k) % n; t += fu[i] - bu[i]
            if t < 0: break
        else:
            return s
    return -1
ok = True
for _ in range(4000):
    n = R.randint(1, 7)
    fu = [R.randint(0, 4) for _ in range(n)]; bu = [R.randint(0, 4) for _ in range(n)]
    if mL(fu, bu) != brute_loop(fu, bu): ok = False
check('loop-depots: model is the smallest working depot on 4000 random loops (notes[1] true)', ok)

# 6. dsa-window-every-venue: model against all-windows brute force, ties included.
mw = model('dsa-window-every-venue')['tightest_window']
def brute_win(feeds):
    best = None
    xs = sorted(set(x for fd in feeds for x in fd))
    for lo in xs:
        for hi in xs:
            if hi < lo: continue
            if all(any(lo <= x <= hi for x in fd) for fd in feeds):
                if best is None or (hi - lo, lo) < (best[1] - best[0], best[0]): best = [lo, hi]
                break
    return best
ok = True
for _ in range(3000):
    k = R.randint(1, 4)
    feeds = [sorted(R.randint(0, 9) for _ in range(R.randint(1, 4))) for _ in range(k)]
    if mw(feeds) != brute_win(feeds) or MC['tightest_window'](feeds) != brute_win(feeds): ok = False
check('window-every-venue: model and mine equal brute force on 3000 random small feed sets', ok)

# 7. dsa-swapped-levels: model against brute force on random swapped BSTs.
ms = model('dsa-swapped-levels')['swapped_levels']
def build(vals):
    if not vals: return None
    i = R.randrange(len(vals))
    return [vals[i], build(vals[:i]), build(vals[i + 1:])]
def freeze(t):
    return None if t is None else (t[0], freeze(t[1]), freeze(t[2]))
def nodes(t, out):
    if t is not None:
        out.append(t); nodes(t[1], out); nodes(t[2], out)
ok = True
for _ in range(3000):
    n = R.randint(0, 9)
    t = build(sorted(R.sample(range(-20, 20), n)))
    ns = []; nodes(t, ns)
    exp = []
    if len(ns) >= 2 and R.random() < 0.8:
        a, c = R.sample(ns, 2); a[0], c[0] = c[0], a[0]; exp = sorted([a[0], c[0]])
    if ms(freeze(t)) != exp: ok = False
check('swapped-levels: model equals the planted swap on 3000 random trees', ok)

# 8. dsa-split-prices notes[2]: work against output size on a branchy input with no answer.
src = json.load(open(os.path.join(DD, 'dsa-split-prices.json')))['solution']
src = src.replace('    def place(pos):\n', '    def place(pos):\n        CALLS[0] += 1\n')
ns = {'CALLS': [0]}
exec(src, ns)
arg = ('1' * 29 + '000', 15, 999)
r = ns['split_prices'](*arg)
calls = ns['CALLS'][0]
check('split-prices: %r, k=15, cap=999 returns [] (model %s, mine %s) after %d calls, against notes[2] "close to the size of the output"' % (arg[0], r, MD['split_prices'](*arg), calls),
      r == [] == MD['split_prices'](*arg) and calls == 3465622)

# 9. dsa-server-loads notes[2]: branches on the hidden tests.
src = json.load(open(os.path.join(DD, 'dsa-server-loads.json')))['solution']
src = src.replace('    def place(i):\n        nonlocal best\n', '    def place(i):\n        nonlocal best\n        CALLS[0] += 1\n')
ns = {'CALLS': [0]}
exec(src, ns)
most = 0
for t in json.load(open(os.path.join(DD, 'dsa-server-loads.json')))['tests']:
    ns['CALLS'][0] = 0
    eval(t['call'], ns)
    most = max(most, ns['CALLS'][0])
check('server-loads: most branches on any hidden test %d, against notes[2] "a few thousand"' % most, most == 133981)
ok = True
mm = model('dsa-server-loads')['min_peak_load']
for _ in range(400):
    jobs = [R.randint(1, 20) for _ in range(R.randint(0, 6))]; k = R.randint(1, 4)
    bf = 0 if not jobs else min(max(sum(j for j, s in zip(jobs, a) if s == q) for q in range(k)) for a in itertools.product(range(k), repeat=len(jobs)))
    if mm(jobs, k) != bf or MD['min_peak_load'](jobs, k) != bf: ok = False
check('server-loads: model and mine equal every-assignment brute force on 400 random cases', ok)

# 11. dsa-swapped-levels constraint: O(n h) in-order by list concatenation, timed on the hidden tests.
w4 = wrong(WC, 'dsa-swapped-levels', '4')['swapped_levels']
d = json.load(open(os.path.join(DD, 'dsa-swapped-levels.json')))
t0 = time.time()
okk = all(eval(t['call'], dict(w4=w4, swapped_levels=w4)) == eval(t['expect']) for t in d['tests'])
check('swapped-levels: the O(n h) concatenation reading passes all 13 tests in %.2fs natively' % (time.time() - t0), okk)

# 12. dsa-feed-passes notes[0]: a cheapest plan need not start a pass on the first needed day, but one always can.
mfp = model('dsa-feed-passes')['solve_feed_passes']
check('feed-passes: "1 9 1 9\\n5\\n" -> 1, the 7-day pass; buying it on day 3 costs the same 1, so "must start on the first needed day" is too strong', mfp('1 9 1 9\n5\n') == '1')

# 13. dsa-footpath-slabs: recurrence check by brute-force tiling for n <= 10.
def tilings(n):
    # columns 0..n-1, two rows; fill leftmost empty cell
    from functools import lru_cache
    @lru_cache(None)
    def go(i, top, bot):
        # top/bot: whether column i's cells are already filled
        if i == n:
            return 1 if not top and not bot else 0
        if top and bot:
            return go(i + 1, False, False)
        tot = 0
        if not top and not bot:
            tot += go(i + 1, False, False)  # one slab across
            if i + 1 < n:
                tot += go(i + 1, True, True)  # square
        if not top and i + 1 < n:
            tot += go(i, True, bot) if False else 0
        return tot
    # simpler exhaustive: count tilings of a 2 x n board by 1x2 dominoes and 2x2 squares
    cells = [(r, c) for c in range(n) for r in range(2)]
    def rec(filled):
        for cell in cells:
            if cell not in filled:
                r, c = cell
                break
        else:
            return 1
        tot = 0
        if r == 0 and (1, c) not in filled:
            tot += rec(filled | {(0, c), (1, c)})
        if c + 1 < n and (r, c + 1) not in filled:
            tot += rec(filled | {(r, c), (r, c + 1)})
        if r == 0 and c + 1 < n and not ({(1, c), (0, c + 1), (1, c + 1)} & filled):
            tot += rec(filled | {(0, c), (1, c), (0, c + 1), (1, c + 1)})
        return tot
    return rec(frozenset())
fw = model('dsa-footpath-slabs')['footpath_ways']
check('footpath: model equals exhaustive tiling for n = 0..10', all(fw(n) == tilings(n) for n in range(11)))


# 14. Proposed replacement for dsa-peak-calls: longest stretch with at least k calls live.
def stretch_fast(text):
    t = list(map(int, text.split())); n, k = t[0], t[1]
    ev = {}
    for i in range(n):
        s0, e0 = t[2 + 2 * i], t[3 + 2 * i]
        ev[s0] = ev.get(s0, 0) + 1
        ev[e0] = ev.get(e0, 0) - 1
    live = 0; start = None; best = 0
    for x in sorted(ev):
        live += ev[x]  # every event at one second applied before the test
        if live >= k and start is None: start = x
        if live < k and start is not None:
            best = max(best, x - start); start = None
    return str(best)
def stretch_brute(text):
    t = list(map(int, text.split())); n, k = t[0], t[1]
    calls = [(t[2 + 2 * i], t[3 + 2 * i]) for i in range(n)]
    hi = max([e for _, e in calls] or [0])
    best = run = 0
    for sec in range(hi + 1):
        if sum(1 for a0, b0 in calls if a0 <= sec < b0) >= k: run += 1; best = max(best, run)
        else: run = 0
    return str(best)
def stretch_ends_first(text):  # the trap: test after each single event, ends first
    t = list(map(int, text.split())); n, k = t[0], t[1]
    ev = sorted([(t[2 + 2 * i], 1) for i in range(n)] + [(t[3 + 2 * i], -1) for i in range(n)])
    live = 0; start = None; best = 0
    for x, d in ev:
        live += d
        if live >= k and start is None: start = x
        if live < k and start is not None: best = max(best, x - start); start = None
    return str(best)
ok = True
for _ in range(1500):
    n = R.randint(1, 6); k = R.randint(1, 3)
    cs = []
    for _ in range(n):
        a0 = R.randint(0, 12); cs.append((a0, a0 + R.randint(1, 8)))
    txt = '%d %d\n' % (n, k) + ''.join('%d %d\n' % c for c in cs)
    if stretch_fast(txt) != stretch_brute(txt): ok = False
check('peak-calls replacement: sweep equals per-second brute force on 1500 random logs', ok)
e1 = '3 2\n0 10\n5 15\n10 20\n'
check('peak-calls replacement example %r -> 10 (sweep %s, brute %s), ends-first trap gives %s' % (e1, stretch_fast(e1), stretch_brute(e1), stretch_ends_first(e1)),
      stretch_fast(e1) == stretch_brute(e1) == '10' and stretch_ends_first(e1) == '5')
e2 = '2 2\n0 5\n5 9\n'
check('peak-calls replacement example %r -> 0 (sweep %s, brute %s)' % (e2, stretch_fast(e2), stretch_brute(e2)), stretch_fast(e2) == stretch_brute(e2) == '0')

e3 = '2 1\n0 5\n5 9\n'
check('peak-calls replacement example %r -> 9 (sweep %s, brute %s), ends-first trap gives %s' % (e3, stretch_fast(e3), stretch_brute(e3), stretch_ends_first(e3)),
      stretch_fast(e3) == stretch_brute(e3) == '9' and stretch_ends_first(e3) == '5')

# 15. Proposed replacement for dsa-upstream-stations: stations on some route from s to r.
def on_route_fast(n, pipes, s0, r0):
    fw = [[] for _ in range(n)]; bw = [[] for _ in range(n)]
    for a0, b0 in pipes: fw[a0].append(b0); bw[b0].append(a0)
    def reach(adj, x):
        seen = [False] * n; seen[x] = True; st = [x]
        while st:
            u = st.pop()
            for v in adj[u]:
                if not seen[v]: seen[v] = True; st.append(v)
        return seen
    f, b = reach(fw, s0), reach(bw, r0)
    return [v for v in range(n) if f[v] and b[v]] if f[r0] else []
def on_route_brute(n, pipes, s0, r0):
    adj = [[] for _ in range(n)]
    for a0, b0 in pipes: adj[a0].append(b0)
    def can(x, y):
        seen = {x}; st = [x]
        while st:
            u = st.pop()
            if u == y: return True
            for v in adj[u]:
                if v not in seen: seen.add(v); st.append(v)
        return False
    if not can(s0, r0): return []
    return [v for v in range(n) if can(s0, v) and can(v, r0)]
ok = True
for _ in range(1500):
    n = R.randint(1, 7)
    pipes = [(R.randrange(n), R.randrange(n)) for _ in range(R.randint(0, 10))]
    s0, r0 = R.randrange(n), R.randrange(n)
    if on_route_fast(n, pipes, s0, r0) != on_route_brute(n, pipes, s0, r0): ok = False
check('upstream replacement: two searches equal pairwise reachability on 1500 random networks', ok)
P = [(0, 1), (1, 2), (3, 2), (2, 4), (5, 0)]
check('upstream replacement example s=5, r=2 -> [0, 1, 2, 5] (fast %s, brute %s)' % (on_route_fast(6, P, 5, 2), on_route_brute(6, P, 5, 2)),
      on_route_fast(6, P, 5, 2) == on_route_brute(6, P, 5, 2) == [0, 1, 2, 5])
check('upstream replacement example s=4, r=2 -> [] (fast %s, brute %s)' % (on_route_fast(6, P, 4, 2), on_route_brute(6, P, 4, 2)),
      on_route_fast(6, P, 4, 2) == on_route_brute(6, P, 4, 2) == [])

# 16. dsa-ticker-batches notes[1]: updating the end only at each ticker's first appearance is still right.
mt = model('dsa-ticker-batches')['ticker_batches']
def first_only(tape):
    last = {c: i for i, c in enumerate(tape)}; seen = set(); out = []; start = end = 0
    for i, c in enumerate(tape):
        if c not in seen: seen.add(c); end = max(end, last[c])
        if i == end: out.append(i - start + 1); start = i + 1
    return out
ok = all(mt(t) == first_only(t) for t in (''.join(R.choice('ABCD') for _ in range(R.randint(0, 10))) for _ in range(3000)))
check('ticker-batches: updating the end only at a ticker\'s first trade equals the model on 3000 tapes (notes[1] wording)', ok)

# 17. dsa-range-volumes notes[1]: rise[l - 1] overcounts only when bar l beat bar l - 1.
mr = model('dsa-range-volumes')['solve_range_volumes']
wr = wrong(WD, 'dsa-range-volumes', '1')['solve_range_volumes']
check('range-volumes: "5 1\\n5 1 4 2 6\\n3 5\\n" gives 1, and the rise[l - 1] slip gives 2 (it also counts bar 3, which beat bar 2)', mr('5 1\n5 1 4 2 6\n3 5\n') == '1' and wr('5 1\n5 1 4 2 6\n3 5\n') == '2')
check('range-volumes: query 2 5 gives 2 with and without the slip (bar 2 did not beat bar 1)', mr('5 1\n5 1 4 2 6\n2 5\n') == wr('5 1\n5 1 4 2 6\n2 5\n') == '2')

print('checks failed:', bad)
sys.exit(1 if bad else 0)
