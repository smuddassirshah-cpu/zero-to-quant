"""Recompute every figure of graphs-dp homework-2 item h-cheapest-count (performance task, L2).

Route 1: the item's own solution (Dijkstra with a heap, counts carried on each venue).
Route 2: Bellman-Ford costs, then counts summed over the tight links in order of cost.
Route 3: small tests by listing every simple route; the ladder by a layer-by-layer table.
Every expectation must agree. Also: the starter fails; each planted wrong solution fails
first at the test its byKey names; a list-scan Dijkstra (slow but correct) passes; the counts
in prose, how and byKey match the file. Run: python3 -I docs/reports/graphs-dp-2-perf-numbers.py
"""
import json, os, signal, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'graphs-dp', 'homework-2.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-cheapest-count']
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
T = w['tests']
print('item index (1-based):', idx[0] + 1, 'of', len(items))


# ---- grading, as js/engine/widgets/code.js does it ----
class Slow(Exception):
    pass


def _alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, _alarm)


def same(x, y):
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
    return bool(x == y)


def namespace(code):
    ns = {'__name__': '__main__', '__learner_source__': code}
    exec(code, ns)
    exec(w['postlude'], ns)
    return ns


def run_tests(code, limit=5.0):
    bad, secs = [], []
    try:
        ns = namespace(code)
    except Exception:
        return list(range(1, len(T) + 1)), []
    for k, t in enumerate(T, 1):
        signal.setitimer(signal.ITIMER_REAL, limit)
        t0 = time.perf_counter()
        try:
            ok = same(eval(t['call'], ns), eval(t['expect'], ns))
        except (Exception, Slow):
            ok = False
        signal.setitimer(signal.ITIMER_REAL, 0)
        secs.append(time.perf_counter() - t0)
        if not ok:
            bad.append(k)
    return bad, secs


# ---- route 2: Bellman-Ford, then counting over tight links ----
def ref_count(links, src, dst):
    INF = float('inf')
    nodes = {src, dst} | {a for a, _, _ in links} | {b for _, b, _ in links}
    cost = {u: INF for u in nodes}
    cost[src] = 0
    for _ in range(len(nodes)):
        changed = False
        for a, b, f in links:
            if cost[a] + f < cost[b]:
                cost[b] = cost[a] + f
                changed = True
        if not changed:
            break
    if cost[dst] == INF:
        return (None, 0)
    ways = {u: 0 for u in nodes}
    ways[src] = 1
    into = {u: [] for u in nodes}
    for a, b, f in links:
        if cost[a] + f == cost[b]:
            into[b].append(a)
    for u in sorted((u for u in nodes if cost[u] < INF), key=lambda u: cost[u]):
        if u != src:
            ways[u] = sum(ways[a] for a in into[u])
    return (cost[dst], ways[dst])


# ---- route 3a: every simple route, small cases ----
def brute_count(links, src, dst):
    out = {}
    for a, b, f in links:
        out.setdefault(a, []).append((b, f))
    totals = []

    def walk(u, seen, c):
        if u == dst:
            totals.append(c)
            return
        for v, f in out.get(u, []):
            if v not in seen:
                walk(v, seen | {v}, c + f)

    walk(src, {src}, 0)
    if not totals:
        return (None, 0)
    best = min(totals)
    return (best, totals.count(best))


sol_ns = namespace(w['solution'])
ref_ns = dict(sol_ns)
ref_ns['count_cheapest'] = ref_count
brute_ns = dict(sol_ns)
brute_ns['count_cheapest'] = brute_count

# 1. Every expectation by two routes (three for the small tests and the ladder).
for k, t in enumerate(T, 1):
    want = eval(t['expect'])
    a = eval(t['call'], sol_ns)
    b = eval(t['call'], ref_ns)
    ok = same(a, want) and same(b, want)
    extra = ''
    if k <= 9:
        ok = ok and same(eval(t['call'], brute_ns), want)
        extra = ' and every simple route listed'
    check(ok, f'test {k}: file {t["expect"]}, solution and Bellman-Ford agree{extra}')

# route 3b: the ladder layer by layer (each layer only links to the next).
links = eval('venue_ladder()', sol_ns)
best = {'L00_0': (0, 1)}
for i in range(60):
    nxt = {}
    for a, b, f in links:
        if a.startswith('L%02d_' % i) and a in best:
            c, n = best[a][0] + f, best[a][1]
            if b not in nxt or c < nxt[b][0]:
                nxt[b] = (c, n)
            elif c == nxt[b][0]:
                nxt[b] = (c, nxt[b][1] + n)
    best = nxt
check(best['L60_0'] == eval(T[10]['expect']), f'ladder by layers: {best["L60_0"]} matches test 11')
check(best['L60_0'][1] == 358584264000 and best['L60_0'][1] > 10 ** 9, 'test 11 count is 358,584,264,000, past a billion (prose)')

# 2. Counts in the file.
check(len(T) == 11 and len(w['examples']) == 1 and w['examples'][0] == T[0], '11 tests, 1 example (test 1)')
check('Check runs 11 hidden tests' in w['how'], 'how: 11 tests')
web = eval('venue_web()', sol_ns)
check(len({x for a, b, _ in web for x in (a, b)}) <= 1000 and len(web) == 6000, 'venue_web(): 1,000 venue names, 6,000 links')
check(len({(a, b) for a, b, _ in web}) == 6000 and all(a != b for a, b, _ in web), 'venue_web(): no repeated link, no self-link')
check(all(1 <= f for _, _, f in web + links), 'every fee in both helpers is at least 1')
layers = {a.split('_')[0] for a, _, _ in links} | {b.split('_')[0] for _, b, _ in links}
check(len(layers) == 61 and len(links) == 60 * 25, 'venue_ladder(): 61 layers of 5 venues, 1,500 links')
check('1,000 venues and 6,000 links' in w['how'] and '61 layers of 5 venues' in w['how'], 'how names 1,000, 6,000, 61 and 5')
for k in range(1, 10):
    L = eval(T[k - 1]['call'].split('count_cheapest(')[1].rsplit(', ', 2)[0])
    check(len({(a, b) for a, b, _ in L}) == len(L) and all(f >= 1 for *_, f in L), f'test {k}: links distinct, fees at least 1')
check(len(items) == 9 and sum(1 for it in items if it.get('performance')) == 1, 'homework-2 holds 9 items (cap 12), one performance item')

# 3. Starter fails.
st_bad, _ = run_tests(w['starter'])
check(len(st_bad) == len(T), f'starter fails tests {st_bad}')

# 4. Planted wrong solutions, by exact text changes to the solution.
S = w['solution']
NOSTALE = ("        if d > cost[u]:\n            continue                # a stale entry: u left the heap earlier\n", "")
TIE = "            elif nd == cost[v]:\n                ways[v] += ways[u]  # a tie: every cheapest route to u extends\n"
plants = {
    'counts arrivals, not routes': ([("                ways[v] = ways[u]\n", "                ways[v] = 1\n"), ("ways[v] += ways[u]  #", "ways[v] += 1  #")], 2),
    'a tie pushes the venue again': ([(TIE, TIE + "                heapq.heappush(heap, (nd, v))\n")], 2),
    'no reset on a cheaper cost': ([("                ways[v] = ways[u]\n", "                ways[v] = ways.get(v, 0) + ways[u]\n")], 3),
    'a venue is fixed when first reached': ([("            if v not in cost or nd < cost[v]:\n", "            if v not in cost:\n")], 3),
    'stale entry expanded again': ([NOSTALE, ("            nd = d + fee\n", "            nd = cost[u] + fee\n")], 5),
    'links read both ways': ([("        adj.setdefault(a, []).append((b, fee))\n", "        adj.setdefault(a, []).append((b, fee))\n        adj.setdefault(b, []).append((a, fee))\n")], 7),
    'returns inf when unreachable': ([("    return None, 0\n", "    return float('inf'), 0\n")], 7),
}
caught_by_example = {
    'ties ignored': ([(TIE, "")], 1),
    'returns on first reaching dst': ([("                cost[v] = nd        # a cheaper route: the old count is void\n",
                                        "                cost[v] = nd        # a cheaper route: the old count is void\n                if v == dst:\n                    return nd, ways[u]\n")], 1),
}
harmless = {'stale entry kept but read with d': ([NOSTALE], None)}


def build(pairs):
    c = S
    for old, new in pairs:
        assert c.count(old) == 1, old
        c = c.replace(old, new)
    return c


firsts = set()
for group, named in ((plants, True), (caught_by_example, False), (harmless, None)):
    for name, (pairs, first) in group.items():
        bad, _ = run_tests(build(pairs))
        if named is None:
            check(bad == [], f'"{name}" is correct: it passes every test')
            continue
        check(bool(bad) and bad[0] == first, f'plant "{name}" first fails test {bad[:1]} (named {first}); fails {bad}')
        if named:
            firsts.add(first)
            check(1 not in bad, f'plant "{name}" passes the example')
plants_code = {
    'KeyError when dst is in no link': ('''import heapq
def count_cheapest(links, src, dst):
    nodes = {src} | {a for a, b, f in links} | {b for a, b, f in links}
    adj = {u: [] for u in nodes}
    for a, b, f in links:
        adj[a].append((b, f))
    cost = {u: float('inf') for u in nodes}
    ways = {u: 0 for u in nodes}
    cost[src], ways[src] = 0, 1
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if d > cost[u]:
            continue
        for v, f in adj[u]:
            if d + f < cost[v]:
                cost[v], ways[v] = d + f, ways[u]
                heapq.heappush(h, (d + f, v))
            elif d + f == cost[v]:
                ways[v] += ways[u]
    return (None, 0) if cost[dst] == float('inf') else (cost[dst], ways[dst])
''', 8),
}
for name, (code, first) in plants_code.items():
    bad, _ = run_tests(code)
    firsts.add(first)
    check(bool(bad) and bad[0] == first and 1 not in bad, f'plant "{name}" first fails test {bad[:1]} (named {first}); fails {bad}')
keyed = {int(k.split('-')[1]) for k in item['feedback']['byKey']}
check(keyed - {4, 11} == firsts, f'byKey tests {sorted(keyed)}: the plants\' first failures {sorted(firsts)}, plus 4 (dst reached dear first) and 11 (the ladder)')

# 5. Slow but correct: Dijkstra that scans a list for the cheapest venue, no heap.
scan = '''def count_cheapest(links, src, dst):
    adj, nodes = {}, {src, dst}
    for a, b, f in links:
        adj.setdefault(a, []).append((b, f))
        nodes.update((a, b))
    INF = float('inf')
    cost = {u: INF for u in nodes}
    ways = {u: 0 for u in nodes}
    cost[src], ways[src] = 0, 1
    done = set()
    while True:
        u = None
        for x in nodes:
            if x not in done and cost[x] < INF and (u is None or cost[x] < cost[u]):
                u = x
        if u is None:
            break
        done.add(u)
        for v, f in adj.get(u, []):
            if cost[u] + f < cost[v]:
                cost[v], ways[v] = cost[u] + f, ways[u]
            elif cost[u] + f == cost[v]:
                ways[v] += ways[u]
    return (None, 0) if cost[dst] == INF else (cost[dst], ways[dst])
'''
bad, secs = run_tests(scan)
check(bad == [], f'list-scan Dijkstra passes every test, slowest {max(secs):.3f} s in CPython')
bad, secs = run_tests(S)
check(bad == [], f'solution passes every test, slowest {max(secs):.3f} s in CPython (limit 5 s)')
enum = 'def count_cheapest(links, src, dst):\n' + '\n'.join('    ' + l for l in '''out = {}
for a, b, f in links:
    out.setdefault(a, []).append((b, f))
totals = []
def walk(u, seen, c):
    if u == dst:
        totals.append(c)
        return
    for v, f in out.get(u, []):
        if v not in seen:
            walk(v, seen | {v}, c + f)
walk(src, {src}, 0)
if not totals:
    return (None, 0)
return (min(totals), totals.count(min(totals)))'''.split('\n')) + '\n'
bad, _ = run_tests(enum, limit=2.0)
check(bad and all(k >= 10 for k in bad), f'listing every route passes tests 1 to 9 and stops on the large maps {bad} (timing only, not a slip)')

# 6. Figures in the byKey text.
E = lambda k: tuple(eval(T[k - 1]['expect']))
check(E(2) == (4, 2 * 2), 'test 2: 2 x 2 = 4 routes reach OSL')
check(E(3) == (3, 1) and 1 + 1 == 2 and 5 > 2, 'test 3: PAR first for 5, then 1 + 1 = 2 through FRA; answer (3, 1)')
check(E(4) == (2, 1) and 1 + 1 == 2 < 9, 'test 4: AMS first for 9, then 1 + 1 = 2 through PAR')
check(E(5) == (7, 1) and 1 + 1 == 2 < 3 and 2 + 5 == 7, 'test 5: ROM from 3 to 2, AMS at 7 by one route')
check(E(7) == (None, 0) and E(8) == (None, 0) and E(9) == (0, 1), 'tests 7, 8: (None, 0); test 9: (0, 1)')
check('358,584,264,000' in item['feedback']['byKey']['test-11'], 'test 11 byKey names 358,584,264,000')

print('failures:', fails)
sys.exit(1 if fails else 0)
