"""Recompute every figure of graphs-dp homework-1 item h-split-desks (performance task, L1).

Route 1: the item's own solution (BFS with a queue). Route 2: an independent union-find with a
parity bit per desk, then the canonical rule (first desk by name in each linked set is group 0).
Route 3, small tests only: brute force over every 0/1 assignment. Every expectation must agree.
Also: the starter fails; each planted wrong solution fails first at the test its byKey names;
two slow but correct solutions pass; the counts in prose, how and byKey match the file.
Run: python3 -I docs/reports/graphs-dp-1-perf-numbers.py
"""
import itertools, json, os, signal, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'graphs-dp', 'homework-1.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-split-desks']
fails = 0


def check(ok, msg):
    global fails
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails += 1


check(len(idx) == 1, 'item present once')
item = items[idx[0]]
w = item['widget']
print('item index (1-based):', idx[0] + 1, 'of', len(items))


# ---- grading, as js/engine/widgets/code.js does it (code, then postlude; eval call; equal) ----
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
    sys.setrecursionlimit(1000)
    bad, secs = [], []
    try:
        ns = namespace(code)
    except Exception:
        return list(range(1, len(w['tests']) + 1)), []
    for k, t in enumerate(w['tests'], 1):
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


# ---- route 2: union-find with parity ----
def ref_split(desks, conflicts):
    parent = {d: d for d in desks}
    parity = {d: 0 for d in desks}          # parity to parent

    def find(x):
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root, acc = x, 0
        for y in reversed(path):            # compress, keeping parity to the root
            acc ^= parity[y]
            parity[y] = acc
            parent[y] = root
        return root

    def par(x):
        find(x)
        return parity[x] if parent[x] != x else 0

    for a, b in conflicts:
        ra, rb = find(a), find(b)
        pa, pb = par(a), par(b)
        if ra == rb:
            if pa == pb:
                return None
        else:
            parent[ra] = rb
            parity[ra] = pa ^ pb ^ 1
    first = {}
    for d in sorted(desks):
        first.setdefault(find(d), d)
    return {d: par(d) ^ par(first[find(d)]) for d in desks}


# ---- route 3: brute force over all assignments (small cases) ----
def brute_split(desks, conflicts):
    order = sorted(desks)
    found = []
    for bits in itertools.product((0, 1), repeat=len(order)):
        g = dict(zip(order, bits))
        if all(g[a] != g[b] for a, b in conflicts):
            found.append(g)
    if not found:
        return None
    # linked sets by plain reachability
    adj = {d: set() for d in desks}
    for a, b in conflicts:
        adj[a].add(b)
        adj[b].add(a)
    comp, seen = {}, set()
    for d in order:
        if d in seen:
            continue
        stack, members = [d], []
        seen.add(d)
        while stack:
            u = stack.pop()
            members.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        for m in members:
            comp[m] = d                      # d is the first desk by name of its set
    canon = [g for g in found if all(g[comp[d]] == 0 for d in desks)]
    return canon[0] if len(canon) == 1 else ('not unique', len(canon))


sol_ns = namespace(w['solution'])
ref_ns = dict(sol_ns)
ref_ns['split_desks'] = ref_split
brute_ns = dict(sol_ns)
brute_ns['split_desks'] = brute_split

# 1. Every expectation by two routes (three for the nine small tests).
for k, t in enumerate(w['tests'], 1):
    want = eval(t['expect'], sol_ns)
    a = eval(t['call'], sol_ns)
    b = eval(t['call'], ref_ns)
    ok = same(a, want) and same(b, want)
    if k <= 9:
        c = eval(t['call'], brute_ns)
        ok = ok and same(c, want)
    check(ok, f'test {k}: file {t["expect"][:60]}, solution and union-find agree' + (' and brute force' if k <= 9 else ''))

# 2. Counts in the file.
T = w['tests']
check(len(T) == 12 and len(w['examples']) == 1 and w['examples'][0] == T[0], '12 tests, 1 example (test 1)')
check('Check runs 12 hidden tests' in w['how'] and 'Tests 10 to 12' in w['how'], 'how: 12 tests, tests 10 to 12 are the large ones')
names, pairs = eval('desk_chain()', sol_ns)
check(len(names) == 3000 and len(pairs) == 2999, 'desk_chain(): 3,000 desks in one chain (2,999 conflicts)')
names, pairs = eval('desk_web()', sol_ns)
adj = {d: [] for d in names}
for a, b in pairs:
    adj[a].append(b)
    adj[b].append(a)
seen, sets = set(), 0
for d in names:
    if d not in seen:
        sets += 1
        seen.add(d)
        stack = [d]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
check(len(names) == 5000 and sets == 3, f'desk_web(): 5,000 desks in {sets} linked sets (how says three)')
check('5,000 desks' in item['prose'] and '3,000 of them' in item['prose'], 'prose: 5,000 desks and a chain through 3,000')
chain_tally = eval(T[9]['expect'])
check(chain_tally == [3000, 1500, 1500, sum(range(1, 3000, 2))], f'test 10 tally {chain_tally}: odd-numbered desks are group 1, sum {sum(range(1, 3000, 2))}')
web_tally = eval(T[10]['expect'])
check(web_tally[0] == 5000 and web_tally[1] + web_tally[2] == 5000, f'test 11 tally {web_tally}: groups add to 5,000')
check(len(items) == 9 and sum(1 for it in items if it.get('performance')) == 1, 'homework-1 holds 9 items (cap 12), one performance item')

# 3. Starter fails.
st_bad, _ = run_tests(w['starter'])
check(len(st_bad) >= 1, f'starter fails tests {st_bad}')

# 4. Planted wrong solutions: each first fails at the named test.
S = w['solution']
plants = {}
text_plants = {
    'conflict stored one way': ("        adj[b].append(a)\n", "", 2),
    'no check on placed neighbours': ("                elif group[v] == group[u]:\n                    return None     # an odd loop: no split works\n", "", 3),
    'returns False, not None': ("return None     #", "return False     #", 3),
    'searches the first set only': ("for start in sorted(desks):", "for start in sorted(desks)[:1]:", 4),
    'desks with no conflict left out': (
        "    adj = {d: [] for d in desks}\n    for a, b in conflicts:          # a conflict runs both ways\n        adj[a].append(b)\n        adj[b].append(a)\n",
        "    adj = {}\n    for a, b in conflicts:\n        adj.setdefault(a, []).append(b)\n        adj.setdefault(b, []).append(a)\n    desks = list(adj)\n", 5),
    'desks taken in the given order': ("for start in sorted(desks):", "for start in desks:", 6),
}
for name, (old, new, first_fail) in text_plants.items():
    check(S.count(old) == 1, f'plant "{name}": text found once')
    plants[name] = (S.replace(old, new), first_fail)
plants['any placed neighbour but the parent is a clash'] = ('''from collections import deque
def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b)
        adj[b].append(a)
    group, parent = {}, {}
    for start in sorted(desks):
        if start in group:
            continue
        group[start], parent[start] = 0, None
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in group:
                    group[v], parent[v] = 1 - group[u], u
                    q.append(v)
                elif v != parent[u]:
                    return None
    return group
''', 7)
plants['greedy, one conflict at a time'] = ('''def split_desks(desks, conflicts):
    group = {}
    for a, b in conflicts:
        if a not in group and b not in group:
            group[a], group[b] = 0, 1
        elif b not in group:
            group[b] = 1 - group[a]
        elif a not in group:
            group[a] = 1 - group[b]
        elif group[a] == group[b]:
            return None
    for d in desks:
        group.setdefault(d, 0)
    return group
''', 8)
plants['recursive search'] = ('''def split_desks(desks, conflicts):
    adj = {d: [] for d in desks}
    for a, b in conflicts:
        adj[a].append(b)
        adj[b].append(a)
    group = {}
    def visit(u):
        for v in adj[u]:
            if v not in group:
                group[v] = 1 - group[u]
                if not visit(v):
                    return False
            elif group[v] == group[u]:
                return False
        return True
    for s in sorted(desks):
        if s not in group:
            group[s] = 0
            if not visit(s):
                return None
    return group
''', 10)
firsts = set()
for name, (code, first_fail) in plants.items():
    bad, _ = run_tests(code)
    firsts.add(bad[0] if bad else None)
    check(bool(bad) and bad[0] == first_fail, f'plant "{name}" first fails test {bad[:1]} (named {first_fail}); fails {bad}')
    check(1 not in bad or first_fail == 1, f'plant "{name}" passes the example')
keyed = {int(k.split('-')[1]) for k in item['feedback']['byKey']}
check(keyed - {9} == firsts, f'byKey tests {sorted(keyed)} are the first failures of the plants {sorted(firsts)}, plus test 9 (an odd loop in a second set)')

# 5. Slow but correct solutions pass; CPython times.
slow = {
    'list as queue, pop(0)': S.replace("from collections import deque\n", "").replace("queue = deque([start])", "queue = [start]").replace("queue.popleft()", "queue.pop(0)"),
    'stack (depth first)': S.replace("u = queue.popleft()", "u = queue.pop()"),
}
for name, code in slow.items():
    check(code != S, f'{name}: built')
    bad, secs = run_tests(code)
    check(bad == [], f'{name}: passes every test, slowest {max(secs):.3f} s in CPython')
bad, secs = run_tests(S)
check(bad == [], f'solution passes every test, slowest {max(secs):.3f} s in CPython (limit 5 s)')

# 6. Figures in the byKey text.
G = lambda k: eval(T[k - 1]['expect'])
check(G(2) == {'Bonds': 0, 'Cash': 1, 'Loans': 1}, 'test 2: Bonds 0, Cash 1, Loans 1')
check(G(3) is None and G(9) is None, 'tests 3 and 9: no split (loops of three)')
check(G(5)['Cash'] == 0, 'test 5: Cash, with no conflicts, is group 0')
check(G(6) == {'Credit': 0, 'Swaps': 0, 'Rates': 1}, 'test 6: Credit and Swaps 0, Rates 1')
check(G(7) == {'Credit': 0, 'FX': 0, 'Equity': 1, 'Rates': 1}, 'test 7: Credit and FX 0, Equity and Rates 1')
greedy = plants['greedy, one conflict at a time'][0]
gns = {}
exec(greedy.replace('        elif group[a] == group[b]:\n            return None\n', '        elif group[a] == group[b]:\n            return dict(group)\n'), gns)
g8 = gns['split_desks'](['Bonds', 'Cash', 'Gilts', 'Loans'], [('Bonds', 'Cash'), ('Gilts', 'Loans'), ('Cash', 'Loans')])
check(g8['Cash'] == 1 and g8['Loans'] == 1, 'test 8: one conflict at a time puts Cash and Loans both in group 1')
check('3,000' in item['feedback']['byKey']['test-10'], 'test 10 byKey names the 3,000-desk chain')

print('failures:', fails)
sys.exit(1 if fails else 0)
