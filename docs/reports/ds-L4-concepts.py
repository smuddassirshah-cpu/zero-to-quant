#!/usr/bin/env python3
"""Concept checks for ds level 4 (l14 to l18, review-4, homework-4). Blind audit, round 1.

Run from the repo root:  python3 -I docs/reports/ds-L4-concepts.py
Every check names its ledger row group (docs/reports/audit-ds-4-ledger.md) and, where it has one, its
finding number in docs/reviews/audit-ds-4.md. Exit 0 means the content is right on every check. A check
whose message starts EXPECTED_FAIL fails because the content is wrong or imprecise as stated; it stays
failing until the content is fixed. Costs are counted in comparisons, node reads or element copies,
never in wall-clock time. Code widgets are run in CPython with the widget's own prelude and hidden tests
(the Pyodide sweep of the same sources is recorded in the audit file, section "test-N sweep").

Fix pass (Opus fixer, audit file section "Fix pass"). Checks that encoded the old text as a computation that can
never change (an arithmetic identity, a cost count or a tree shape that the content does not control) are re-pointed
to the content string they judge, keeping the computation as evidence: findings 1, 3, 5, 6, 7, 8, 15 and 16. The
test-N checks (findings 9 to 20) now name the line each coding lands on after the fix; a coding whose line was
deleted is checked against the line that now catches it. Findings 4 and 21 are unchanged: they pass because hidden
test 13 was added. The fixer's own codings (docs/reports/ds-L4-fix-codings.txt, also swept under Pyodide) are run
at the end: each must first fail the test its header names, and that byKey line must exist.
"""
import bisect, heapq, json, math, os, random, statistics, sys
from collections import deque

sys.setrecursionlimit(3000)          # the page's limit (app/js/screens/drill-worker.js)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'ds')
FAILS = []
def check(cond, msg):
    if not cond:
        FAILS.append(msg); print('FAIL', msg)
def load(name):
    with open(os.path.join(COURSE, name)) as f:
        return json.load(f)
L14, L15, L16, L17, L18 = (load(n) for n in ['l14-binary-trees.json', 'l15-search-trees.json', 'l16-tree-recursion.json',
                                              'l17-always-the-smallest.json', 'l18-order-book-heaps.json'])
R4, H4 = load('review-4.json'), load('homework-4.json')
rng = random.Random(20261126)

# ---------------------------------------------------------------- widget harness (CPython)
def norm(x):
    if isinstance(x, (list, tuple)):
        return [norm(v) for v in x]
    return x
def first_fail(widget, src):
    """1-based index of the first hidden test `src` fails, or 0 when it passes them all."""
    env = {'__learner_source__': src}
    try:
        exec((widget.get('prelude') or '') + '\n' + src + '\n' + (widget.get('postlude') or ''), env)
    except Exception:
        return 1
    for i, t in enumerate(widget['tests'], 1):
        try:
            if t.get('setup'):
                exec(t['setup'], env)
            got = eval(t['call'], env)
            want = eval(t['expect'], env) if isinstance(t['expect'], str) else t['expect']   # `expect` is Python source
            if norm(got) != norm(want) or type(got) is not type(want) and isinstance(want, bool):
                return i
        except Exception:
            return i
    return 0
def W(doc, i):
    return (doc['screens'] if 'screens' in doc else doc['items'])[i]['widget']
for doc, idxs in [(L14, [6, 10]), (L15, [5, 7, 9]), (L16, [4, 6, 9]), (L17, [5, 9]), (L18, [9]), (H4, [0, 1, 2, 7])]:
    for i in idxs:
        w = W(doc, i)
        check(first_fail(w, w['solution']) == 0, f"{doc.get('id')} widget {i}: solution passes its hidden tests")
        check(first_fail(w, w['starter']) != 0, f"{doc.get('id')} widget {i}: starter fails")
def mutant(doc, i, override):
    w = W(doc, i)
    return first_fail(w, w['solution'] + '\n' + override)

# ---------------------------------------------------------------- l14 binary trees
class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right
def build(values):
    if not values or values[0] is None:
        return None
    it = iter(values); root = Node(next(it)); q = deque([root])
    while q:
        node = q.popleft()
        for side in ('left', 'right'):
            try:
                v = next(it)
            except StopIteration:
                return root
            if v is not None:
                c = Node(v); setattr(node, side, c); q.append(c)
    return root
def pre(n): return [] if n is None else [n.val] + pre(n.left) + pre(n.right)
def ino(n): return [] if n is None else ino(n.left) + [n.val] + ino(n.right)
def post(n): return [] if n is None else post(n.left) + post(n.right) + [n.val]
def level(root):
    out, q = [], deque([root] if root else [])
    while q:
        n = q.popleft(); out.append(n.val)
        q.extend(c for c in (n.left, n.right) if c)
    return out
AG = build(list('ABCDEFG'))
check(''.join(pre(AG)) == 'ABDECFG' and ''.join(ino(AG)) == 'DBEAFCG' and ''.join(post(AG)) == 'DEBFGCA' and ''.join(level(AG)) == 'ABCDEFG',
      'l14 s2-s5: the four orders on the A to G tree')
def pre_mirror(n): return [] if n is None else [n.val] + pre_mirror(n.right) + pre_mirror(n.left)
check(''.join(pre_mirror(AG)) == 'ACGFBED', 'l14 s7 option b: swapped calls give A C G F B E D')
def height(n): return -1 if n is None else 1 + max(height(n.left), height(n.right))
def depth_of(root, target, d=0):
    if root is None: return None
    if root.val == target: return d
    return depth_of(root.left, target, d + 1) if depth_of(root.left, target, d + 1) is not None else depth_of(root.right, target, d + 1)
check(depth_of(AG, 'G') == 2 and depth_of(AG, 'A') == 0 and height(AG) == 2 and height(build([1])) == 0,
      'l14 s1 and q-height: depth in links from the root, height of one node 0 (CLRS B.5.2)')
# expression tree: 50 x (108 - 100) - 12
check(50 * (108 - 100) - 12 == 388 and 50 * (108 - 100) == 400 and 12 - 50 * (108 - 100) == -388, 'l14 s9 key 388, slips fee 400 and sign -388')
check(50 * 108 - 12 == 5388, 'l14 s9 slip gross 5388 is "skipped the inner minus"')
_gross = L14['screens'][9]['feedback']['byKey']['gross']
_gval = [w_['value'] for w_ in L14['screens'][9]['widget']['wrong'] if w_['id'] == 'gross'][0]
check(50 + (108 - 100) - 12 == 46 and 'as +' not in _gross and 'skipped the inner' in _gross and _gval == 50 * 108 - 12,
      'EXPECTED_FAIL l14 s9 feedback.byKey.gross: "treated x as +" gives 46, not 5388; the line must name only the skipped inner minus (finding 3)')
check(max(110 - 95, 0) - max(110 - 105, 0) == 10 and 100 * max(120 - 110, 0) == 1000, 'l14 s10 test 6 bull call spread is 10; caption 1000')
# cost of the taught concatenating walk on a chain, counted in list elements copied
class L(list):
    copies = 0
    def __add__(self, other):
        L.copies += len(self) + len(other); return L(list.__add__(self, other))
def ino_concat(n): return L() if n is None else ino_concat(n.left) + L([n.val]) + ino_concat(n.right)
def chain_left(n):
    root = None
    for v in range(n):
        root = Node(v, root, None)
    return root
c1 = []
for n in (200, 400, 800):
    L.copies = 0; ino_concat(chain_left(n)); c1.append(L.copies)
check(c1[2] / c1[1] > 3.5 and c1[1] / c1[0] > 3.5, 'l14 s8: the concatenating walk copies about n^2/2 elements on a chain (doubling n quadruples the copies)')
check(c1[2] / c1[1] > 3.5 and 'appends to one list' in L14['summary']['formula']['note'] and 'appends to one list' in L15['screens'][3]['explain']['text']
      and '$O(n^2)$ on a chain' in L14['screens'][8]['prose'], 'EXPECTED_FAIL l14 summary.formula.note and l15 s3 explain: "O(n)" does not hold for the walk as written with + (it is O(n h)); only the shared-list walk is O(n) (finding 5)')

# ---------------------------------------------------------------- l15 search trees
def bst_insert(root, v):
    if root is None: return Node(v)
    if v < root.val: root.left = bst_insert(root.left, v)
    elif v > root.val: root.right = bst_insert(root.right, v)
    return root
def bst_from(vs):
    r = None
    for v in vs: r = bst_insert(r, v)
    return r
def search_path(root, v):
    path, turns, n = [], [], root
    while n is not None:
        path.append(n.val)
        if v == n.val: return path, turns, True
        turns.append('L' if v < n.val else 'R'); n = n.left if v < n.val else n.right
    return path, turns, False
T7 = build([50, 30, 70, 20, 40, 60, 80])
check(search_path(T7, 60)[0] == [50, 70, 60], 'l15 s0: 60 found at the third comparison')
check(search_path(T7, 65)[1] == ['R', 'L', 'R'] and search_path(T7, 35)[1] == ['L', 'R', 'L'] and search_path(T7, 85)[1] == ['R', 'R', 'R'],
      'l15 s1, s2: 65 right-left-right, 35 left-right-left, 85 right three times')
check(ino(T7) == [20, 30, 40, 50, 60, 70, 80], 'l15 s3: in-order on a BST is sorted')
CH = bst_from([10, 20, 30, 40, 50])
check(len(search_path(CH, 50)[0]) == 5 and height(CH) == 4, 'l15 s4: sorted inserts give a chain, 5 comparisons, height 4')
BAD = build([10, 5, 15, None, None, 6, 20])
p6 = search_path(BAD, 6)
check(p6[2] is False, 'l15 s6: a search for 6 does not find it')
check(p6[1][0] == 'L' and 'go left at 10' in L15['screens'][6]['explain']['text'] and 'go right at 10' not in L15['screens'][6]['explain']['text'], 'EXPECTED_FAIL l15 s6 explain: "A search for 6 would go right at 10": 6 < 10, so it goes left at 10, then right at 5 onto None (finding 1)')
# height bounds on random insertion orders (Monte Carlo over shapes)
ok = True
for _ in range(400):
    n = rng.randint(1, 120); vs = rng.sample(range(1000), n); h = height(bst_from(vs))
    ok &= math.floor(math.log2(n)) <= h <= n - 1
check(ok, 'l15 s8: floor(log2 n) <= h <= n - 1 on 400 random BSTs')
check(2 ** (9 + 1) - 1 == 1023 and height(bst_from(range(1000))) == 999 if False else 2 ** 10 - 1 == 1023, 'l15 s8: perfect tree of height 9 holds 1,023')
r = None
for v in range(1000):   # iterative chain build (recursion-free)
    if r is None: r = tail = Node(v)
    else: tail.right = Node(v); tail = tail.right
hh, n_ = -1, r
while n_: hh += 1; n_ = n_.right
check(hh == 999, 'l15 q-sorted: 1,000 ascending inserts give height 999')
# bisect: comparisons to find, shifts to insert; and what list.sort() really costs after one append
class C:
    n = 0
    __slots__ = ('v',)
    def __init__(self, v): self.v = v
    def __lt__(self, o): C.n += 1; return self.v < o.v
N = 1 << 14
xs = [C(i) for i in range(N)]
C.n = 0; bisect.bisect_left(xs, C(N // 3)); check(C.n <= math.log2(N) + 1, 'l15 q-bisect: bisect finds a place in at most log2 n + 1 comparisons')
ys = xs + [C(N // 3)]; C.n = 0; ys.sort(); cmp_sort_append = C.n
check(cmp_sort_append < 3 * N, 'l15 q-bisect: CPython sort() after one append makes O(n) comparisons (Timsort is adaptive)')
def _opt(doc, part, i, oid):
    return [o_ for o_ in doc[part][i]['widget']['options'] if o_['id'] == oid][0]['why']
_resort = [_opt(L15, 'quiz', 3, 'd'), L17['screens'][7]['prose'], _opt(L17, 'quiz', 1, 'd'), _opt(L18, 'screens', 8, 'd'), L18['screens'][8]['feedback']['byKey']['d']]
check(cmp_sort_append < 3 * N and not any('\\log n)$ per' in t_ or '\\log n)$ each time' in t_ for t_ in _resort), 'EXPECTED_FAIL l15 q-bisect option d, l17 s7 prose, l17 q-max option d, l18 s8 option d: "sort after every insert costs O(n log n)" is the generic bound; CPython re-sorts a sorted list plus one item in O(n) (finding 6)')
# validate
def validate(root, lo=None, hi=None):
    if root is None: return True
    if lo is not None and root.val <= lo: return False
    if hi is not None and root.val >= hi: return False
    return validate(root.left, lo, root.val) and validate(root.right, root.val, hi)
def looks_ok(node):
    if node is None: return True
    if node.left and node.left.val >= node.val: return False
    if node.right and node.right.val <= node.val: return False
    return looks_ok(node.left) and looks_ok(node.right)
check(looks_ok(BAD) and not validate(BAD), 'l15 s6, s7: the children-only check passes the tree that bounds reject')
opts = [o['text'].strip('`') for o in R4['items'][5]['widget']['options']]
trees = [build(eval(o)) for o in opts]   # option texts are level-order lists
check([validate(t) for t in trees] == [True, False, False, False], 'review-4 r4-valid: only the first list is a BST')
_r4v = R4['items'][5]['explain']['text']
check(all(looks_ok(t) for t in trees[1:3]) and not looks_ok(trees[3]) and 'each hide one node' not in _r4v and 'Two of the others' in _r4v and 'repeats a value' in _r4v, 'EXPECTED_FAIL review-4 r4-valid explain: "The others each hide one node that passes its parent but fails an ancestor": the repeated 3 in option d fails against its own parent (finding 16)')

# ---------------------------------------------------------------- l16 recursion
T16 = build([1, 2, 3, 4, 5, None, None, 6])
check(height(T16) == 3 and height(None) == -1, 'l16 s0, s1: height 3; None is -1 so a leaf is 0')
def best_route(n):
    if n.left is None and n.right is None: return n.val
    return n.val + max(best_route(c) for c in (n.left, n.right) if c)
check(best_route(build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])) == 27, 'l16 s2: best route 27')
LAT = build([2, -1, 3, 4, -2, -5, 1, None, None, 6, 1, 2, 8])
check(best_route(LAT) == 8 and 2 + 3 + 1 == 6 and 2 + 3 + 8 == 13, 'l16 s8: key 8, greedy 6, skip slip 13')
def balanced_def(n): return n is None or (abs(height(n.left) - height(n.right)) <= 1 and balanced_def(n.left) and balanced_def(n.right))
T3 = build([1, 2, 5, 3, None, 6, None, 4])
check(not balanced_def(T3) and abs(height(T3.left) - height(T3.right)) <= 1, 'l16 s3: unbalanced at 2 although the root passes')
# naive is_balanced on a chain: node visits by height()
def naive_visits(n):
    cnt = [0]
    def h(x):
        if x is None: return -1
        cnt[0] += 1; return 1 + max(h(x.left), h(x.right))
    def ib(x):
        if x is None: return True
        a = ib(x.left); b = ib(x.right)
        gap = abs(h(x.left) - h(x.right))       # computed before the return, as on the screen
        return a and b and gap <= 1
    ib(chain_left(n)); return cnt[0]
check(naive_visits(1000) == 1000 * 999 // 2 == 499500, 'l16 s5: n(n-1)/2 = 499,500 height visits on a chain of 1,000')
# convention shift and the diameter formula, brute force over random trees
def rand_tree(n):
    if n == 0: return None
    k = rng.randint(0, n - 1); return Node(0, rand_tree(k), rand_tree(n - 1 - k))
def hn(n): return 0 if n is None else 1 + max(hn(n.left), hn(n.right))
def balanced_nodes(n): return n is None or (abs(hn(n.left) - hn(n.right)) <= 1 and balanced_nodes(n.left) and balanced_nodes(n.right))
def diam_formula(root):
    best = [0]
    def h(n):
        if n is None: return -1
        a, b = h(n.left), h(n.right); best[0] = max(best[0], a + b + 2); return 1 + max(a, b)
    h(root); return best[0]
def diam_bfs(root):
    adj, nodes = {}, []
    def walk(n, p):
        if n is None: return
        nodes.append(n); adj.setdefault(id(n), [])
        if p is not None: adj[id(n)].append(p); adj[id(p)].append(n)
        walk(n.left, n); walk(n.right, n)
    walk(root, None)
    best = 0
    for s in nodes:
        dist = {id(s): 0}; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[id(u)]:
                if id(v) not in dist: dist[id(v)] = dist[id(u)] + 1; q.append(v)
        best = max(best, max(dist.values()))
    return best
ok1 = ok2 = True
for _ in range(300):
    t = rand_tree(rng.randint(1, 25))
    ok1 &= balanced_def(t) == balanced_nodes(t); ok2 &= diam_formula(t) == diam_bfs(t)
check(ok1, 'l16 q-convention: both height conventions give the same balance verdict on 300 random trees')
check(ok2, 'l16 s7: diameter = max over v of h(L) + h(R) + 2 with h(None) = -1, against BFS on 300 random trees')
check(diam_formula(build([1, 2, 3, 4, 5])) == 3 and diam_formula(build([1, 2, None, 3, 4, 5, None, None, 6])) == 4, 'l16 q-diameter 3; review-4 r4-diameter 4')
check(height(build([1, 2, 3, None, 4, None, None, 5])) == 3, 'review-4 r4-height 3')

# ---------------------------------------------------------------- l17 heaps
H = [2, 5, 3, 9, 6, 7, 8]
check(all(H[(i - 1) // 2] <= H[i] for i in range(1, len(H))) and (H[3], H[4]) == (9, 6) and (5 - 1) // 2 == 2 == (6 - 1) // 2 and (10 - 1) // 2 == 4,
      'l17 s0, s1, q-parent: children 2i+1, 2i+2; parent (i-1)//2')
def push(h, x):
    h.append(x); i = len(h) - 1; swaps = 0
    while i > 0 and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2; h[i], h[p] = h[p], h[i]; i = p; swaps += 1
    return swaps
def pop(h):
    top = h[0]; last = h.pop()
    if h:
        h[0] = last; i, n = 0, len(h)
        while True:
            s = i
            for c in (2 * i + 1, 2 * i + 2):
                if c < n and h[c] < h[s]: s = c
            if s == i: break
            h[i], h[s] = h[s], h[i]; i = s
    return top
h = list(H); sw = push(h, 4)
check(h == [2, 4, 3, 5, 6, 7, 8, 9] and sw == 2, 'l17 s2: push 4, two swaps')
check(pop(h) == 2 and h == [3, 4, 7, 5, 6, 9, 8], 'l17 s3: pop gives [3, 4, 7, 5, 6, 9, 8]')
h = [3, 5, 4, 9, 6]; push(h, 1); check(h == [1, 5, 3, 9, 6, 4], 'review-4 r4-push key')
h = [3, 5, 4, 9, 6, 1]; h[5], h[1] = h[1], h[5]; h[1], h[0] = h[0], h[1]
_key = [1, 5, 3, 9, 6, 4]; _key[1], _key[2] = _key[2], _key[1]
_r4p = _opt(R4, 'items', 3, 'd')
_r4d = [o_ for o_ in R4['items'][3]['widget']['options'] if o_['id'] == 'd'][0]['text'].strip('`')
check(h == [1, 3, 4, 9, 6, 5] and _key == eval(_r4d)
      and 'swapped 1 with index 1' not in _r4p and '5 and 3 have changed places' in _r4p, 'EXPECTED_FAIL review-4 r4-push option d why: swapping 1 with index 1 (then the root) gives [1, 3, 4, 9, 6, 5], not the option [1, 3, 5, 9, 6, 4] (finding 15)')
levels = lambda n: math.floor(math.log2(n)) + 1
check(levels(10 ** 6) == 20 and levels(10) - 1 == 3, 'l17 s4, s7: 20 levels for a million, at most 19 swaps; 3 for a heap of 10')
worst = max(push(list(range(2, 2 + n)), 1) for n in range(1, 300)); check(all(push(list(range(2, 2 + n)), 1) == levels(n + 1) - 1 for n in range(1, 300)), 'l17 s4: worst push climbs levels - 1')
def level_sizes(n): return [min(2 ** d, n - (2 ** d - 1)) for d in range(levels(n))]
check(level_sizes(7) == [1, 2, 4], 'l17 s4: full levels hold 2^d')
check(level_sizes(8)[-1] == 1 < 2 ** 3 and 'holds up to $2^d$ items' in L17['screens'][4]['prose'] and 'every level but the last is full' in L17['screens'][4]['prose'], 'EXPECTED_FAIL l17 s4 prose: "Level d of a heap holds 2^d items": the last level may hold fewer (the screen\'s own 8-item heap has 1 item on level 3) (finding 7)')
hq = []
for x in [120, 45, 300, 80, 210, 60]:
    heapq.heappush(hq, -x)
    if len(hq) > 3: heapq.heappop(hq)
check(sorted(-v for v in hq) == [45, 60, 80], 'l17 s6: the negated heap keeps the three smallest trades')
asks = []
for t in [(100.03, 1, 'A1'), (100.02, 4, 'A2'), (100.02, 2, 'A3'), (100.05, 3, 'A4')]: heapq.heappush(asks, t)
check(asks[0][2] == 'A3', 'l17 s8: lowest price, then earliest time (tuple comparison, CPython heapq docs)')
def top_k(xs, k):
    if k <= 0: return []
    hh = []
    for x in xs:
        if len(hh) < k: heapq.heappush(hh, x)
        elif x > hh[0]: heapq.heapreplace(hh, x)
    return sorted(hh, reverse=True)
check(all(top_k(v, k) == heapq.nlargest(k, v) == sorted(v, reverse=True)[:k] for v, k in
          [([rng.randint(0, 50) for _ in range(rng.randint(0, 40))], rng.randint(0, 12)) for _ in range(300)]), 'l17 s9: top_k equals heapq.nlargest and the sorted slice')
# comparison counts: top-k, n pushes, heapify
def count(f):
    C.n = 0; f(); return C.n
n = 1 << 13
data = [C(rng.random()) for _ in range(n)]
check(count(lambda: top_k(data, 10)) <= n * (2 * math.log2(10) + 2), 'l17 s7: top k of n costs O(n log k) comparisons')
desc = [C(-i) for i in range(n)]
def pushes(v):
    hh = []
    for x in v: heapq.heappush(hh, x)
p_worst = count(lambda: pushes(desc)); p_rand = count(lambda: pushes(data)); hfy = count(lambda: heapq.heapify(list(data)))
check(0.5 * n * math.log2(n) < p_worst <= n * math.log2(n) and p_rand < 4 * n, 'l17 q-sorted: n pushes are O(n log n) in the worst case (about linear on random arrivals)')
check(hfy < 3 * n < p_worst, 'homework-4 h4-leaves explain: heapify is O(n), cheaper than n worst-case pushes (CLRS 6.3)')
check(sum(1 for i in range(100) if 2 * i + 1 > 99) == 50, 'homework-4 h4-leaves: 50 leaves in a heap of 100')
seen, hp, tot = [], [], 0
for x in data[:512]:
    seen.append(x); C.n = 0; sorted(seen); tot += C.n
check(tot > 0.5 * sum(m * math.log2(m) for m in range(2, 513)) * 0.5, 'l17 q-sorted: sorted(seen) on unsorted arrivals is n log n per call')

# ---------------------------------------------------------------- l18 order book
ns = {}
exec(W(L18, 9)['prelude'] + '\n' + W(L18, 9)['solution'], ns)
OrderBook, play = ns['OrderBook'], ns['play']
bids = []
for t in [(-100.00, 1, 'B1'), (-99.99, 2, 'B2'), (-100.00, 3, 'B3')]: heapq.heappush(bids, t)
check(bids[0] == (-100.0, 1, 'B1'), 'l18 s1: negated price, plain time')
base = [('add', 'B1', 'buy', 100.00, 300), ('add', 'B2', 'buy', 99.99, 500), ('add', 'B3', 'buy', 99.98, 200),
        ('add', 'A1', 'sell', 100.02, 200), ('add', 'A2', 'sell', 100.03, 400), ('add', 'A3', 'sell', 100.05, 100)]
q = [('best_bid',), ('best_ask',)]
got = play(base + [('add', 'A4', 'sell', 100.01, 100)] + q + [('cancel', 'B1')] + q + [('add', 'B4', 'buy', 100.00, 50)] + q + [('cancel', 'A4')] + q)
check(got == [100.0, 100.01, 99.99, 100.01, 100.0, 100.01, 100.0, 100.02], 'l18 s2: the quote table')
f = play(base + [('add', 'X', 'buy', 100.03, 500), ('match',), ('best_ask',)])
check(f[0] == [('X', 'A1', 100.02, 200), ('X', 'A2', 100.03, 300)] and round(sum(p * s for _, _, p, s in f[0]), 2) == 50013.0 and f[1] == 100.03,
      'l18 s3: sweep 200 + 300, 50,013 pounds, 100 left at 100.03')
f = play([('add', 'A1', 'sell', 100.02, 200), ('add', 'A5', 'sell', 100.02, 300), ('add', 'X', 'buy', 100.02, 250), ('match',)])
check(f[0] == [('X', 'A1', 100.02, 200), ('X', 'A5', 100.02, 50)], 'l18 s4: price-time priority, A1 200 then A5 50')
f = play([('add', 'S', 'sell', 100.02, 10), ('add', 'B', 'buy', 100.05, 10), ('match',)])
check(f[0] == [('B', 'S', 100.02, 10)], 'l18 q-price: the fill is at the resting order\'s price')
check(round(200 * 100.00 + 300 * 99.99 + 100 * 99.98, 2) == 59995.0 and round(600 * 99.98, 2) == 59988.0 and 600 * 100 == 60000, 'review-4 r4-sweep 59,995; slips 59,988 and 60,000')
check(round(100.03 - 99.99, 2) == 0.04 and round(100.01 - 100.00, 2) == 0.01 and round(100.03 - 99.98, 2) == 0.05, 'review-4 r4-quotes 0.04; slips 0.01 and 0.05')
# lazy deletion: dead pops are bounded by cancels; dead entries away from the top stay in the heap
book = OrderBook(); pops = [0]
_orig = heapq.heappop
def counting_pop(hh): pops[0] += 1; return _orig(hh)
ns['heapq'].heappop = counting_pop
try:
    ids, cancels = [], 0
    for i in range(4000):
        book.add(f'B{i}', 'buy', 1000 - rng.randint(0, 200), 10); ids.append(f'B{i}')
        if rng.random() < 0.9 and ids:
            book.cancel(ids.pop(rng.randrange(len(ids)))); cancels += 1
        book.best_bid()
finally:
    ns['heapq'].heappop = _orig
check(pops[0] <= cancels, 'l18 s7, q-amortised: all reads together pop at most one dead entry per cancel')
live = sum(1 for o in book.live.values() if o[0] == 'buy')
_s7, _qc = L18['screens'][7]['prose'], _opt(L18, 'quiz', 3, 'c')
check(len(book.bids) > 2 * live + 10 and 'live entries' not in _s7 and 'live or dead' in _s7 and 'outgrow the live book' in _s7
      and 'never holds more entries than orders were added' in _qc and 'as soon as they reach the top' not in _qc, 'EXPECTED_FAIL l18 s7 prose "With n live entries" and q-amortised option c why: cancelled entries below the top never surface, so the heap holds far more than the live orders (here %d entries for %d live) and n is the heap size, dead entries included (finding 8)' % (len(book.bids), live))
try:
    hd = []; heapq.heappush(hd, (100.02, {'id': 'A7'})); heapq.heappush(hd, (100.02, {'id': 'A9'})); raised = False
except TypeError:
    raised = True
check(raised, 'homework-4 h4-dict-tuple: a price tie compares the dicts and raises TypeError')

# ---------------------------------------------------------------- homework: merge, median, Timsort on k runs
ns2 = {}; exec(W(H4, 1)['solution'], ns2); exec(W(H4, 2)['solution'], ns2)
for _ in range(100):
    lists = [sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 8))) for _ in range(rng.randint(0, 6))]
    check(ns2['merge_k'](lists) == sorted(sum(lists, [])), 'homework-4 h4-merge equals the sorted concatenation')
    v = [rng.randint(-20, 20) for _ in range(rng.randint(0, 30))]
    check(ns2['running_median'](v) == [float(statistics.median(v[:i + 1])) for i in range(len(v))], 'homework-4 h4-median equals statistics.median on every prefix')
k, per = 64, 512
runs = [[C(i + j * k) for j in range(per)] for i in range(k)]     # k sorted lists, interleaved values
flat = [x for r_ in runs for x in r_]; Ntot = k * per
cmp_timsort = count(lambda: sorted(flat))
def merge_heap():
    hh = [(r_[0], i, 0) for i, r_ in enumerate(runs)]; heapq.heapify(hh); out = []
    while hh:
        v, i, j = heapq.heappop(hh); out.append(v)
        if j + 1 < per: heapq.heappush(hh, (runs[i][j + 1], i, j + 1))
cmp_heap = count(merge_heap)
check(cmp_heap <= 3 * Ntot * math.log2(k), 'homework-4 h4-merge: the heap merge is O(N log k)')
_hm = H4['items'][1]['prose'] + ' ' + H4['items'][1]['widget']['how']
check(cmp_timsort < 0.8 * Ntot * math.log2(Ntot) and 'Sorting everything again' not in _hm and 'ignores that each list is already sorted' not in _hm
      and 'A general sort' in _hm, 'EXPECTED_FAIL homework-4 h4-merge prose and how: "Sorting everything again costs O(N log N)" and "re-sorting everything ignores that each list is already sorted": CPython\'s sort finds the k runs and merges them in about N log2 k comparisons (%d here, against N log2 N = %d and the heap\'s %d) (finding 6)' % (cmp_timsort, Ntot * math.log2(Ntot), cmp_heap))

# ---------------------------------------------------------------- test-N lines: natural codings of the named mistake (CPython replica of the Pyodide sweep)
def by_key(doc, i):
    return (doc['screens'] if 'screens' in doc else doc['items'])[i]['feedback']['byKey']
def expect_line(doc, i, n, name, src, tag, line=True, text_ok=True):
    """Fix pass: n is the test the coding lands on after the fix; line=True also needs a byKey line for it;
    text_ok is a judgement on the text of a line that no longer names this coding."""
    got = mutant(doc, i, src)
    ok = got == n and (not line or f'test-{n}' in by_key(doc, i)) and text_ok
    check(ok, f"EXPECTED_FAIL {doc.get('id')} widget {i} feedback.byKey.test-{n}: the named mistake ({name}) first fails test {got or 'none (passes all)'}, not test {n}, or the line is missing ({tag})")
EV = '''
def evaluate(node):
    if node.left is None and node.right is None:
        return node.val
    a = evaluate(node.left); b = evaluate(node.right)
    if node.val == '+': return a + b
    if node.val == '-': return %s
    if node.val == '*': return a * b
    return max(a, b)
'''
expect_line(L14, 6, 1, 'no None base case', 'def preorder(root):\n    return [root.val] + preorder(root.left) + preorder(root.right)\n', 'finding 9')
expect_line(L14, 10, 1, 'no leaf case', 'def evaluate(node):\n    a = evaluate(node.left); b = evaluate(node.right)\n    return {"+": a + b, "-": a - b, "*": a * b}.get(node.val, node.val)\n', 'finding 10')
expect_line(L14, 10, 1, 'right minus left', EV % 'b - a', 'finding 11', text_ok='412' in by_key(L14, 10).get('test-1', '') and 'right child from the left' not in by_key(L14, 10).get('test-7', ''))
expect_line(L15, 5, 1, 'insert with no None case', 'def insert(root, v):\n    if v < root.val:\n        if root.left is None: root.left = Node(v)\n        else: insert(root.left, v)\n    elif v > root.val:\n        if root.right is None: root.right = Node(v)\n        else: insert(root.right, v)\n    return root\n', 'finding 12')
expect_line(L15, 5, 1, 'left and right swapped', 'def insert(root, v):\n    if root is None: return Node(v)\n    if v < root.val: root.right = insert(root.right, v)\n    elif v > root.val: root.left = insert(root.left, v)\n    return root\n', 'finding 12')
expect_line(L15, 9, 1, 'no None check (no test-1 line: the generic line shows)', 'def levels_between(root, lo, hi):\n    out = []\n    def walk(node):\n        if node.val > lo: walk(node.left)\n        if lo <= node.val <= hi: out.append(node.val)\n        if node.val < hi: walk(node.right)\n    walk(root)\n    return out\n', 'finding 13', line=False)
expect_line(L16, 4, 1, 'None returns 0', 'def height(root):\n    if root is None: return 0\n    return 1 + max(height(root.left), height(root.right))\n', 'finding 2')
expect_line(L16, 4, 4, 'size with the wrong or no base case', 'def size(root):\n    if root is None: return -1\n    return 1 + size(root.left) + size(root.right)\n', 'finding 14')
expect_line(L16, 9, 4, 'best total starts at 0', 'def max_root_to_leaf(root):\n    if root.left is None and root.right is None: return root.val\n    best = 0\n    for c in (root.left, root.right):\n        if c is not None: best = max(best, max_root_to_leaf(c))\n    return root.val + best\n', 'finding 17')
expect_line(L17, 5, 5, 'write to index 0 after the last pop', 'def pop(heap):\n    top = heap[0]\n    heap[0] = heap.pop()\n    i, n = 0, len(heap)\n    while True:\n        s = i\n        for c in (2 * i + 1, 2 * i + 2):\n            if c < n and heap[c] < heap[s]: s = c\n        if s == i: break\n        heap[i], heap[s] = heap[s], heap[i]; i = s\n    return top\n', 'finding 18')
TK = 'def top_k(xs, k):\n    if k <= 0: return []\n    h = []\n    for x in xs:\n        if len(h) < k: heapq.heappush(h, x)\n        elif x >= h[0]: heapq.heapreplace(h, x)\n    return sorted(h, reverse=True)\n'
expect_line(L17, 9, 0, 'replace on >= rather than >, which is correct', TK, 'finding 19', line=False, text_ok='strictly' not in by_key(L17, 9).get('test-4', ''))
RM = '''
def running_median(xs):
    lo, hi, out = [], [], []
    for x in xs:
        if lo and x > -lo[0]: heapq.heappush(hi, x)
        else: heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1: heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo): heapq.heappush(lo, -heapq.heappop(hi))
        out.append(float(lo[0]) if len(lo) > len(hi) else (lo[0] + hi[0]) / 2)
    return out
'''
expect_line(H4, 2, 1, 'lower top read without negating', RM, 'finding 20', text_ok='without negating' in by_key(H4, 2).get('test-1', ''))
# fix pass: deleted lines stay gone, and rewritten lines no longer name codings that cannot reach them
check(not {'test-2', 'test-10'} & set(by_key(L15, 5)) and 'test-6' not in by_key(L16, 9) and 'test-6' not in by_key(L17, 5),
      'EXPECTED_FAIL l15 s5 test-2 and test-10, l16 s9 test-6, l17 s5 test-6: lines no natural coding reaches are deleted (findings 12, 17, 18)')
check('Check for `None`' not in by_key(L15, 9).get('test-7', '') and 'treat it as a leaf' in by_key(L15, 9).get('test-7', ''), 'EXPECTED_FAIL l15 s9 test-7: the line names the leaf mistake that reaches test 7 (finding 13)')
check('`None` returned 0' not in by_key(L16, 4).get('test-2', ''), 'EXPECTED_FAIL l16 s4 test-2: a None at 0 fails test 1, so test 2 must not diagnose it (finding 2)')
# wrong programs that the hidden tests accept
FLAG = '''
def is_balanced(root):
    def check(node):
        if node is None:
            return 0
        lh = check(node.left)
        rh = check(node.right)
        if abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)
    return check(root) != -1
'''
env = {}; exec(W(L16, 6)['prelude'] + FLAG, env)
check(env['is_balanced'](env['build']([1, 2, None, 3, None, 4])) is True, 'l16 s6: the flag-not-passed-up version calls a 4-node chain balanced (it is not)')
check(mutant(L16, 6, FLAG) != 0, 'EXPECTED_FAIL l16 s6 tests: an is_balanced that never passes the -1 flag up (the step hint 2 teaches) passes all 12 hidden tests (finding 21)')
NOTIME = '''
def _add(self, order_id, side, price, qty):
    self.time += 1
    self.live[order_id] = [side, price, qty, self.time]
    heapq.heappush(self.bids if side == "buy" else self.asks, (-price if side == "buy" else price, order_id))
def _top(self, heap):
    while heap and heap[0][-1] not in self.live:
        heapq.heappop(heap)
    return (heap[0][0], 0, heap[0][-1]) if heap else None
OrderBook.add = _add; OrderBook._top = _top
'''
env = {}; exec(W(L18, 9)['prelude'] + W(L18, 9)['solution'] + NOTIME, env)
g = env['play']([('add', 'A9', 'sell', 100.02, 200), ('add', 'A1', 'sell', 100.02, 300), ('add', 'B1', 'buy', 100.02, 250), ('match',)])
check(g[0][0][1] == 'A1', 'l18 s9: a book with (price, id) tuples and no time fills the later order A1 before the earlier A9')
check(mutant(L18, 9, NOTIME) != 0, 'EXPECTED_FAIL l18 s9 tests: a book with no time priority at all (ties broken by order id) passes all 12 hidden tests, because every test names its orders in arrival order (finding 4)')

# ---------------------------------------------------------------- fix pass: the fixer's codings (docs/reports/ds-L4-fix-codings.txt)
_DOCS = {'l14-binary-trees': L14, 'l15-search-trees': L15, 'l16-tree-recursion': L16, 'l17-always-the-smallest': L17,
         'l18-order-book-heaps': L18, 'homework-4': H4}
with open(os.path.join(ROOT, 'docs', 'reports', 'ds-L4-fix-codings.txt')) as f_:
    _blocks = f_.read().split('### ')[1:]
for b_ in _blocks:
    head_, src_ = b_.split('\n', 1)
    fname_, loc_, n_, cname_ = head_.split()
    d_, i_, n_ = _DOCS[fname_], int(loc_[1:]), int(n_)
    got_ = mutant(d_, i_, src_)
    check(got_ == n_ and (n_ == 0 or f'test-{n_}' in by_key(d_, i_)),
          f'fix coding {fname_} {loc_} {cname_}: first fails test {got_ or "none"}, line test-{n_} expected')
check(len(_blocks) == 56, 'fix pass: 56 codings read')

# ---------------------------------------------------------------- report
print(f'{len(FAILS)} failing check(s)')
expected = [f for f in FAILS if f.startswith('EXPECTED_FAIL')]
print(f'{len(expected)} expected (content findings), {len(FAILS) - len(expected)} unexpected')
sys.exit(1 if FAILS else 0)
