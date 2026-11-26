#!/usr/bin/env python3
"""Fix-pass read of ds level 4 (commit dc9834ae): the reader's own checks.

Part A (pure Python): derivations behind the changed sentences and the expected values of the two new hidden tests.
Part B (needs --local-cdn <pkgs>): the reader's own codings of the mistake each new or rewritten `test-N` line names,
graded under the page's Pyodide through app/tools/code-runner.mjs. Each coding states the first failing test it should hit.

  python docs/reports/ds-L4-fixread.py [--local-cdn <pkgs>]

Exit 0 when every check agrees with the content. A check listed in KNOWN stays visible as a finding and does not fail the run.
"""
import heapq, json, math, os, subprocess, sys, tempfile
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DS = os.path.join(ROOT, 'app', 'content', 'courses', 'ds')
bad = []


def check(name, cond, detail=''):
    print(('ok   ' if cond else 'FAIL ') + name + (' | ' + str(detail) if detail else ''))
    if not cond:
        bad.append(name)


def load(f):
    return json.load(open(os.path.join(DS, f + '.json')))


# ---------------------------------------------------------------- Part A
class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build(values):
    if not values or values[0] is None:
        return None
    it = iter(values)
    root = Node(next(it))
    q = deque([root])
    while q:
        node = q.popleft()
        for side in ('left', 'right'):
            try:
                v = next(it)
            except StopIteration:
                return root
            if v is not None:
                child = Node(v)
                setattr(node, side, child)
                q.append(child)
    return root


def h_edges(n):  # CLRS B.5.2: height in edges, empty tree -1
    return -1 if n is None else 1 + max(h_edges(n.left), h_edges(n.right))


def balanced_by_definition(n):  # every node: side heights differ by at most 1
    if n is None:
        return True
    return abs(h_edges(n.left) - h_edges(n.right)) <= 1 and balanced_by_definition(n.left) and balanced_by_definition(n.right)


def first_unbalanced(n):  # deepest-first
    if n is None:
        return None
    return first_unbalanced(n.left) or first_unbalanced(n.right) or (n.val if abs(h_edges(n.left) - h_edges(n.right)) > 1 else None)


# l16 screens[6] hidden test 13
t = build([1, None, 2, 3, None, None, 4, 5])
shape = (t.left is None and t.right.val == 2 and t.right.left.val == 3 and t.right.right is None and t.right.left.left is None
         and t.right.left.right.val == 4 and t.right.left.right.left.val == 5 and t.right.left.right.right is None)
check('l16 s6 test 13: zigzag of five nodes 1 R 2 L 3 R 4 L 5', shape)
check('l16 s6 test 13: expected False by the definition', balanced_by_definition(t) is False)
check('l16 s6 test 13: unbalanced at 3 only', first_unbalanced(t) == 3 and abs(h_edges(t.right.left.left) - h_edges(t.right.left.right)) == 2)
w = load('l16-tree-recursion')['screens'][6]['widget']
check('l16 s6 test 13 authored expect is False', w['tests'][12]['expect'] == 'False' and len(w['tests']) == 13)
# the older unbalanced tests do not need the flag to travel through a node whose sides differ by exactly 1
def no_propagation(root):
    def c(n):
        if n is None:
            return 0
        a, b = c(n.left), c(n.right)
        return -1 if abs(a - b) > 1 else 1 + max(a, b)
    return c(root) != -1
olds = [[1, 2, 2, 3, 3, None, None, 4, 4], [1, 2, 5, 3, None, 6, None, 4], [1, None, 2, None, 3], [1, 2, 3, 4, None, None, None, 5]]
check('l16 s6: a helper that never passes the flag up still answers the four older unbalanced builds', all(no_propagation(build(v)) is False for v in olds))
check('l16 s6: and answers True on test 13 (so only test 13 catches it)', no_propagation(t) is True)


# l18 screens[9] hidden test 13: a reference book with no heap, price then arrival time, fill at the earlier order's price
def ref_play(events):
    live, clock, out = {}, [0], []

    def best(side):
        c = [(-(o[1]) if side == 'buy' else o[1], o[3], i) for i, o in live.items() if o[0] == side]
        return min(c) if c else None

    for name, *a in events:
        if name == 'add':
            clock[0] += 1
            live[a[0]] = [a[1], a[2], a[3], clock[0]]
        elif name == 'cancel':
            live.pop(a[0], None)
        elif name == 'best_bid':
            b = best('buy'); out.append(None if b is None else -b[0])
        elif name == 'best_ask':
            s = best('sell'); out.append(None if s is None else s[0])
        else:
            fills = []
            while True:
                b, s = best('buy'), best('sell')
                if b is None or s is None or -b[0] < s[0]:
                    break
                bo, so = live[b[2]], live[s[2]]
                q = min(bo[2], so[2])
                fills.append((b[2], s[2], bo[1] if bo[3] < so[3] else so[1], q))
                bo[2] -= q; so[2] -= q
                for i in (b[2], s[2]):
                    if live[i][2] == 0:
                        del live[i]
            out.append(fills)
    return out


w18 = load('l18-order-book-heaps')['screens'][9]['widget']
ev13 = [('add', 'A9', 'sell', 100.02, 200), ('add', 'A1', 'sell', 100.02, 300), ('add', 'B1', 'buy', 100.02, 250), ('match',),
        ('add', 'B9', 'buy', 100.0, 100), ('add', 'B2', 'buy', 100.0, 100), ('add', 'A5', 'sell', 100.0, 150), ('match',)]
want13 = [[('B1', 'A9', 100.02, 200), ('B1', 'A1', 100.02, 50)], [('B9', 'A5', 100.0, 100), ('B2', 'A5', 100.0, 50)]]
check('l18 s9 test 13: the authored call is the event list read here', eval(w18['tests'][12]['call'], {'play': lambda e: e}) == ev13)
check('l18 s9 test 13: reference book gives the authored expect', ref_play(ev13) == want13 == eval(w18['tests'][12]['expect']), ref_play(ev13))
check('l18 s9: 13 tests', len(w18['tests']) == 13)
# the reference agrees with every older fixed test too, so it is a fair oracle
agree = all(ref_play(eval(c['call'], {'play': lambda e: e})) == eval(c['expect']) for c in w18['tests'][:11])
check('l18 s9: reference book agrees with authored tests 1 to 11', agree)
# tuple order: heapq compares tuples left to right, so (price, time, id) never reaches the id
hp = []
for e in [(100.02, 1, 'A9'), (100.02, 2, 'A1')]:
    heapq.heappush(hp, e)
check('heap of (price, time, id): the earlier A9 is on top', hp[0][2] == 'A9')
hp = []
for e in [(100.02, 'A9', 1), (100.02, 'A1', 2)]:
    heapq.heappush(hp, e)
check('heap of (price, id, time): the id decides, A1 on top', hp[0][1] == 'A1')

# hw4 items[5]: leaves of a 100-item heap, and the O(n) build
n = 100
leaves = [i for i in range(n) if 2 * i + 1 > n - 1]
check('hw4 i5: leaves are indices 50 to 99, half the heap', leaves == list(range(50, 100)))
check('hw4 i5: last index with a child is 49', max(i for i in range(n) if 2 * i + 1 <= n - 1) == 49)
def sink_room(i, n):  # levels below index i
    d = 0
    while 2 * i + 1 < n:
        i = 2 * i + 1; d += 1
    return d
for m in (100, 10**5):
    rooms = [sink_room(i, m) for i in range(m)]
    check(f'hw4 i5: n={m}: at least 7 in 8 items can sink two levels at most; total sink room below 2n',
          sum(r <= 2 for r in rooms) / m >= 0.87 and sum(rooms) < 2 * m, (round(sum(r <= 2 for r in rooms) / m, 3), sum(rooms)))

# l17 screens[4]: levels of a heap
check('l17 s4: floor(log2 n) + 1 levels for n = 1..5000', all(n.bit_length() == math.floor(math.log2(n)) + 1 for n in range(1, 5001)))
check('l17 s4: every level but the last is full (array heap)', all(sum(1 for i in range(n) if (i + 1).bit_length() - 1 == d) == 2 ** d
                                                                  for n in (6, 100, 1000) for d in range(n.bit_length() - 1)))

# l14 screens[8]: `+` copies; cost on a chain against a balanced tree
def concat_cost(node):  # (length, items copied) for [v] + L + R
    if node is None:
        return 0, 0
    a, ca = concat_cost(node.left); b, cb = concat_cost(node.right)
    return a + b + 1, ca + cb + a + b + 1
def chain(k):
    r = None
    for v in range(k):
        r = Node(v, r)
    return r
c1, c2 = concat_cost(chain(400))[1], concat_cost(chain(800))[1]
check('l14 s8: copies on a chain grow as n^2 (doubling n gives about 4 times)', 3.9 < c2 / c1 < 4.1 and c1 == 400 * 401 // 2, (c1, c2))

# sorting an almost sorted list: comparisons counted
class C:
    n = 0
    def __init__(self, v): self.v = v
    def __lt__(self, o):
        C.n += 1
        return self.v < o.v
import bisect
for m in (1000, 4000):
    xs = [C(i * 2) for i in range(m)]; xs.append(C(m + 1)); C.n = 0; xs.sort(); s = C.n
    ys = [C(i * 2) for i in range(m)]; C.n = 0; bisect.insort(ys, C(m + 1)); b = C.n
    check(f'l15 quiz[3] d: sort() after one append compares about n items ({s}), insort about log2 n ({b}), n={m}', m - 1 <= s <= 2 * m and b <= math.ceil(math.log2(m)) + 1)

# l17 quiz[1] d: a list sorted in reverse, then heappop
h = []
for x in [5, 1, 3, 9, 4]:
    heapq.heappush(h, x); h.sort(reverse=True)
pops = [heapq.heappop(h) for _ in range(5)]
print('     l17 quiz[1] d: push then sort(reverse=True) each time, then five heappops ->', pops)
KNOWN = ['l17 quiz[1] d: after a reverse sort heappop returns the smallest']
check(KNOWN[0], pops[0] == 1, f'first pop is {pops[0]}, the largest; pops {pops}')

# small numbers in the changed feedback
check('l14 s9 gross: 50 x 108 - 12 = 5388, and (108 - 100) x 50 = 400', 50 * 108 - 12 == 5388 and 50 * (108 - 100) == 400
      and any(x['id'] == 'gross' and x['value'] == 5388 for x in load('l14-binary-trees')['screens'][9]['widget']['wrong']))
check('l14 s10 test-1: right minus left at both minus nodes gives 412', 12 - 50 * (100 - 108) == 412)
hp = [3, 5, 4, 9, 6]; heapq.heappush(hp, 1)
check('review-4 i3: push 1 gives [1, 5, 3, 9, 6, 4]; option d has 5 and 3 exchanged', hp == [1, 5, 3, 9, 6, 4])
def is_bst(vals):
    def ok(n, lo, hi):
        return n is None or ((lo is None or n.val > lo) and (hi is None or n.val < hi) and ok(n.left, lo, n.val) and ok(n.right, n.val, hi))
    return ok(build(vals), None, None)
def parent_only(vals):
    def ok(n):
        return n is None or (not (n.left and n.left.val >= n.val) and not (n.right and n.right.val <= n.val) and ok(n.left) and ok(n.right))
    return ok(build(vals))
r5 = {'a': [8, 3, 10, 1, 6, None, 14], 'b': [8, 3, 10, 1, 9, None, 14], 'c': [8, 3, 10, 1, 6, 7, 14], 'd': [8, 3, 10, 3, 6, None, 14]}
check('review-4 i5: a valid; b and c pass the parent check and fail an ancestor; d fails on the repeated 3 at its parent',
      is_bst(r5['a']) and not is_bst(r5['b']) and parent_only(r5['b']) and not is_bst(r5['c']) and parent_only(r5['c']) and not parent_only(r5['d']))
# l15 s6: search for 6 in 10 / (5, 15 / (6, 20))
bt = Node(10, Node(5), Node(15, Node(6), Node(20)))
path, node = [], bt
while node is not None and node.val != 6:
    path.append((node.val, 'left' if 6 < node.val else 'right')); node = node.left if 6 < node.val else node.right
check('l15 s6: a search for 6 goes left at 10 and falls off', path[0] == (10, 'left') and node is None, path)
# hw4 i2: running median by sorting, as an oracle for the two feedback numbers
def med(xs):
    out = []
    for i in range(1, len(xs) + 1):
        s = sorted(xs[:i]); out.append(float(s[i // 2]) if i % 2 else (s[i // 2 - 1] + s[i // 2]) / 2)
    return out
check('hw4 i2: test 1 and test 7 expects', med([5, 15, 1, 3]) == [5.0, 10.0, 5.0, 4.0] and med([-1, -2, -3]) == [-1.0, -1.5, -2.0])

# ---------------------------------------------------------------- Part B: the reader's codings under the page's Pyodide
IO = """
def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def level_order(root):
    out = []
    q = deque([root] if root else [])
    while q:
        node = q.popleft()
        out.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return out
"""
CM = """

def contains(root, v):
    while root is not None and root.val != v:
        root = root.left if v < root.val else root.right
    return root is not None


def min_value(root):
    while root.left is not None:
        root = root.left
    return root.val
"""
HT = """
def height(root):
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))
"""
SZ = """
def size(root):
    if root is None:
        return 0
    return 1 + size(root.left) + size(root.right)
"""
PUSH = """
def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0 and heap[(i - 1) // 2] > heap[i]:
        p = (i - 1) // 2
        heap[i], heap[p] = heap[p], heap[i]
        i = p
"""
SIFT = """
    i, n = 0, len(heap)
    while 2 * i + 1 < n:
        c = 2 * i + 1
        if c + 1 < n and heap[c + 1] < heap[c]:
            c += 1
        if heap[i] <= heap[c]:
            break
        heap[i], heap[c] = heap[c], heap[i]
        i = c
    return top
"""
def med_src(route, odd, even):
    return f"""import heapq

def running_median(xs):
    lo, hi, out = [], [], []
    for x in xs:
        if lo and x > {route}:
            heapq.heappush(hi, x)
        else:
            heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append({odd})
        else:
            out.append({even})
    return out
"""
def ev_src(leaf, minus, pre=''):
    return f"""def evaluate(node):
{pre}{leaf}
    if node.val == '+':
        return a + b
    if node.val == '-':
        return {minus}
    if node.val == '*':
        return a * b
    return max(a, b)
"""
LEAF_OK = "    if node.left is None and node.right is None:\n        return node.val\n    a = evaluate(node.left)\n    b = evaluate(node.right)"
def bal_src(body):
    return f"""def is_balanced(root):
    def check(node):
        if node is None:
            return 0
{body}
        return 1 + max(lh, rh)
    return check(root) != -1
"""
def book_src(bid, ask, idx, extra=''):
    return f"""import heapq

class OrderBook:
    def __init__(self):
        self.bids, self.asks, self.live, self.n = [], [], {{}}, 0

    def add(self, order_id, side, price, qty):
        self.n += 1
        self.live[order_id] = [price, qty, self.n]
        if side == "buy":
            heapq.heappush(self.bids, {bid})
        else:
            heapq.heappush(self.asks, {ask})

    def cancel(self, order_id):
        self.live.pop(order_id, None)

    def _clean(self, heap):
        while heap and heap[0][{idx}] not in self.live:
            heapq.heappop(heap)
        return heap[0][{idx}] if heap else None

    def best_bid(self):
        i = self._clean(self.bids)
        return None if i is None else self.live[i][0]

    def best_ask(self):
        i = self._clean(self.asks)
        return None if i is None else self.live[i][0]

    def match(self):
        fills = []
        while True:
            b, a = self._clean(self.bids), self._clean(self.asks)
            if b is None or a is None or self.live[b][0] < self.live[a][0]:
                return fills
            bo, ao = self.live[b], self.live[a]
            q = min(bo[1], ao[1])
            fills.append((b, a, bo[0] if bo[2] < ao[2] else ao[0], q))
            bo[1] -= q
            ao[1] -= q
            if bo[1] == 0:
                del self.live[b]
            if ao[1] == 0:
                del self.live[a]
"""

# (file, list key, index, the byKey line it belongs to, expected first failing test, label, source)
CODINGS = [
    ('homework-4', 'items', 2, 'test-1', 1, 'odd and even reads use lo[0] as it is', med_src('-lo[0]', 'float(lo[0])', '(lo[0] + hi[0]) / 2')),
    ('homework-4', 'items', 2, 'test-1', 1, 'only the even case forgets to negate', med_src('-lo[0]', 'float(-lo[0])', '(lo[0] + hi[0]) / 2')),
    ('homework-4', 'items', 2, 'test-1', 1, 'even case returns the lower top, no mean', med_src('-lo[0]', 'float(-lo[0])', 'float(-lo[0])')),
    ('homework-4', 'items', 2, 'test-7', 7, 'abs() on the reads only', med_src('-lo[0]', 'float(abs(lo[0]))', '(abs(lo[0]) + hi[0]) / 2')),
    ('homework-4', 'items', 2, 'test-7', 7, 'a "make it positive" helper everywhere', "def pos(v):\n    return -v if v < 0 else v\n\n" + med_src('pos(lo[0])', 'float(pos(lo[0]))', '(pos(lo[0]) + hi[0]) / 2')),

    ('l14-binary-trees', 'screens', 6, 'test-1', 1, 'stack walk that pushes None children', "def preorder(root):\n    out, stack = [], [root]\n    while stack:\n        node = stack.pop()\n        out.append(node.val)\n        stack.append(node.right)\n        stack.append(node.left)\n    return out\n" + IO),
    ('l14-binary-trees', 'screens', 6, 'test-1', 1, 'node placed after its left side', "def preorder(root):\n    if root is None:\n        return []\n    return preorder(root.left) + [root.val] + preorder(root.right)\n" + IO),
    ('l14-binary-trees', 'screens', 6, 'test-5', 5, 'stack walk, children checked, root not', "def preorder(root):\n    out, stack = [], [root]\n    while stack:\n        node = stack.pop()\n        out.append(node.val)\n        if node.right:\n            stack.append(node.right)\n        if node.left:\n            stack.append(node.left)\n    return out\n" + IO),
    ('l14-binary-trees', 'screens', 6, 'test-5', 5, 'inner helper with child checks', "def preorder(root):\n    out = []\n    def go(node):\n        out.append(node.val)\n        if node.left is not None:\n            go(node.left)\n        if node.right is not None:\n            go(node.right)\n    go(root)\n    return out\n" + IO),

    ('l14-binary-trees', 'screens', 10, 'test-4', 4, 'leaf looked for one level down', ev_src("    a = node.left.val if node.left.left is None else evaluate(node.left)\n    b = node.right.val if node.right.left is None else evaluate(node.right)", 'a - b')),
    ('l14-binary-trees', 'screens', 10, 'test-4', 4, 'operands read through a child helper', "def operand(child):\n    if child.left is None and child.right is None:\n        return child.val\n    return evaluate(child)\n\n" + ev_src("    a, b = operand(node.left), operand(node.right)", 'a - b')),
    ('l14-binary-trees', 'screens', 10, 'test-7', 7, 'minus floored with max(.., 0)', ev_src(LEAF_OK, 'max(a - b, 0)')),
    ('l14-binary-trees', 'screens', 10, 'test-7', 7, 'minus floored with an if', ev_src(LEAF_OK, 'a - b if a > b else 0')),
    ('l14-binary-trees', 'screens', 10, 'test-1', 1, 'right minus left', ev_src(LEAF_OK, 'b - a')),
    ('l14-binary-trees', 'screens', 10, 'test-1', 1, 'no leaf case at all', ev_src("    a = evaluate(node.left)\n    b = evaluate(node.right)", 'a - b')),
    ('l14-binary-trees', 'screens', 10, 'test-8', 8, 'leaf told by type(...) is int', ev_src("    if type(node.val) is int:\n        return node.val\n    a = evaluate(node.left)\n    b = evaluate(node.right)", 'a - b')),
    ('l14-binary-trees', 'screens', 10, 'test-8', 8, 'leaf told by str(...).isdigit()', ev_src("    if str(node.val).isdigit():\n        return node.val\n    a = evaluate(node.left)\n    b = evaluate(node.right)", 'a - b')),
    ('l14-binary-trees', 'screens', 10, '(none: note)', 3, "minus as abs(a - b): fails test 3, which has no line", ev_src(LEAF_OK, 'abs(a - b)')),

    ('l15-search-trees', 'screens', 5, 'test-1', 1, 'loop insert with no empty-tree case', "def insert(root, v):\n    node = root\n    while True:\n        if v == node.val:\n            return root\n        side = 'left' if v < node.val else 'right'\n        if getattr(node, side) is None:\n            setattr(node, side, Node(v))\n            return root\n        node = getattr(node, side)\n" + CM),
    ('l15-search-trees', 'screens', 5, 'test-1', 1, 'recursive call result not assigned', "def insert(root, v):\n    if root is None:\n        return Node(v)\n    if v < root.val:\n        insert(root.left, v)\n    elif v > root.val:\n        insert(root.right, v)\n    return root\n" + CM),
    ('l15-search-trees', 'screens', 5, 'test-1', 1, 'smaller sent right, larger left', "def insert(root, v):\n    if root is None:\n        return Node(v)\n    if v < root.val:\n        root.right = insert(root.right, v)\n    elif v > root.val:\n        root.left = insert(root.left, v)\n    return root\n" + CM),

    ('l15-search-trees', 'screens', 9, 'test-7', 7, 'stop at any node with a missing child', "def levels_between(root, lo, hi):\n    out = []\n    def walk(node):\n        if node is None:\n            return\n        if node.left is None or node.right is None:\n            if lo <= node.val <= hi:\n                out.append(node.val)\n            return\n        if node.val > lo:\n            walk(node.left)\n        if lo <= node.val <= hi:\n            out.append(node.val)\n        if node.val < hi:\n            walk(node.right)\n    walk(root)\n    return out\n"),
    ('l15-search-trees', 'screens', 9, 'test-7', 7, 'right side walked only inside the left check', "def levels_between(root, lo, hi):\n    if root is None:\n        return []\n    out = []\n    if root.left is not None:\n        if root.val > lo:\n            out += levels_between(root.left, lo, hi)\n        if lo <= root.val <= hi:\n            out.append(root.val)\n        if root.val < hi:\n            out += levels_between(root.right, lo, hi)\n    elif lo <= root.val <= hi:\n        out.append(root.val)\n    return out\n"),

    ('l16-tree-recursion', 'screens', 4, 'test-2', 2, 'max(..., 0) inside the combine', "def height(root):\n    if root is None:\n        return -1\n    return 1 + max(height(root.left), height(root.right), 0)\n" + SZ),
    ('l16-tree-recursion', 'screens', 4, 'test-2', 2, 'None at -1 on top, nodes counted below', "def height(root):\n    if root is None:\n        return -1\n    def h(node):\n        return 0 if node is None else 1 + max(h(node.left), h(node.right))\n    return h(root)\n" + SZ),
    ('l16-tree-recursion', 'screens', 4, 'test-5', 5, 'stack count, children checked, root not', HT + "\ndef size(root):\n    n, stack = 0, [root]\n    while stack:\n        node = stack.pop()\n        n += 1\n        if node.left:\n            stack.append(node.left)\n        if node.right:\n            stack.append(node.right)\n    return n\n"),
    ('l16-tree-recursion', 'screens', 4, 'test-5', 5, 'conditional expression per child', HT + "\ndef size(root):\n    return 1 + (size(root.left) if root.left else 0) + (size(root.right) if root.right else 0)\n"),
    ('l16-tree-recursion', 'screens', 4, 'test-4', 4, 'size copies the -1 base of height', HT + "\ndef size(root):\n    if root is None:\n        return -1\n    return 1 + size(root.left) + size(root.right)\n"),
    ('l16-tree-recursion', 'screens', 4, 'test-4', 4, 'size copies the max of height', HT + "\ndef size(root):\n    if root is None:\n        return 0\n    return 1 + max(size(root.left), size(root.right))\n"),

    ('l16-tree-recursion', 'screens', 6, 'test-13', 13, 'flag never passed up', bal_src("        lh, rh = check(node.left), check(node.right)\n        if abs(lh - rh) > 1:\n            return -1")),
    ('l16-tree-recursion', 'screens', 6, 'test-13', 13, 'right side checked for the flag first, left never', bal_src("        rh = check(node.right)\n        if rh == -1:\n            return -1\n        lh = check(node.left)\n        if abs(lh - rh) > 1:\n            return -1")),
    ('l16-tree-recursion', 'screens', 6, 'test-13', 13, 'early return for the left flag only', bal_src("        lh = check(node.left)\n        if lh < 0:\n            return -1\n        rh = check(node.right)\n        if abs(lh - rh) > 1:\n            return -1")),

    ('l16-tree-recursion', 'screens', 9, 'test-4', 4, 'missing child read as 0', "def max_root_to_leaf(root):\n    left = max_root_to_leaf(root.left) if root.left else 0\n    right = max_root_to_leaf(root.right) if root.right else 0\n    return root.val + max(left, right)\n"),
    ('l16-tree-recursion', 'screens', 9, 'test-4', 4, 'per-node best started at 0', "def max_root_to_leaf(root):\n    if not root.left and not root.right:\n        return root.val\n    best = 0\n    if root.left:\n        best = max(best, max_root_to_leaf(root.left))\n    if root.right:\n        best = max(best, max_root_to_leaf(root.right))\n    return root.val + best\n"),
    ('l16-tree-recursion', 'screens', 9, '(none: note)', 3, 'one running best over all routes, started at 0: fails test 3, which has no line', "def max_root_to_leaf(root):\n    best = 0\n    def go(node, total):\n        nonlocal best\n        total += node.val\n        if node.left is None and node.right is None:\n            best = max(best, total)\n        if node.left:\n            go(node.left, total)\n        if node.right:\n            go(node.right, total)\n    go(root, 0)\n    return best\n"),
    ('l16-tree-recursion', 'screens', 9, '(none: note)', 6, 'one-child nodes handled, two-child best started at 0: fails test 6, whose line was deleted', "def max_root_to_leaf(root):\n    if root.left is None and root.right is None:\n        return root.val\n    if root.left is None:\n        return root.val + max_root_to_leaf(root.right)\n    if root.right is None:\n        return root.val + max_root_to_leaf(root.left)\n    best = 0\n    for child in (root.left, root.right):\n        best = max(best, max_root_to_leaf(child))\n    return root.val + best\n"),

    ('l17-always-the-smallest', 'screens', 5, 'test-5', 5, 'heap[0] = heap.pop()', PUSH + "\ndef pop(heap):\n    top = heap[0]\n    heap[0] = heap.pop()" + SIFT),
    ('l17-always-the-smallest', 'screens', 5, 'test-5', 5, 'last item saved, then written to index 0', PUSH + "\ndef pop(heap):\n    top = heap[0]\n    last = heap.pop()\n    heap[0] = last" + SIFT),

    ('l17-always-the-smallest', 'screens', 9, 'test-4', 4, 'a value already in the heap is skipped', "import heapq\n\ndef top_k(xs, k):\n    if k <= 0:\n        return []\n    h = []\n    for x in xs:\n        if x in h:\n            continue\n        if len(h) < k:\n            heapq.heappush(h, x)\n        elif x > h[0]:\n            heapq.heapreplace(h, x)\n    return sorted(h, reverse=True)\n"),
    ('l17-always-the-smallest', 'screens', 9, 'test-4', 4, 'a seen-set while streaming', "import heapq\n\ndef top_k(xs, k):\n    if k <= 0:\n        return []\n    h, seen = [], set()\n    for x in xs:\n        if x in seen:\n            continue\n        seen.add(x)\n        heapq.heappush(h, x)\n        if len(h) > k:\n            heapq.heappop(h)\n    return sorted(h, reverse=True)\n"),
    ('l17-always-the-smallest', 'screens', 9, '(control)', 0, 'replace on >= keeps every copy and passes', "import heapq\n\ndef top_k(xs, k):\n    if k <= 0:\n        return []\n    h = []\n    for x in xs:\n        if len(h) < k:\n            heapq.heappush(h, x)\n        elif x >= h[0]:\n            heapq.heapreplace(h, x)\n    return sorted(h, reverse=True)\n"),

    ('l18-order-book-heaps', 'screens', 9, 'test-13', 13, 'heap entries (price, id), time kept in the dict', book_src('(-price, order_id)', '(price, order_id)', 1)),
    ('l18-order-book-heaps', 'screens', 9, 'test-13', 13, 'heap entries (price, id, time)', book_src('(-price, order_id, self.n)', '(price, order_id, self.n)', 1)),
    ('l18-order-book-heaps', 'screens', 9, '(control)', 0, 'heap entries (price, time, id) pass', book_src('(-price, self.n, order_id)', '(price, self.n, order_id)', 2)),
    ('l18-order-book-heaps', 'screens', 9, '(note)', 5, 'newest first at a price, (price, -time, id): test 5 already catches it', book_src('(-price, -self.n, order_id)', '(price, -self.n, order_id)', 2)),
]

MJS = r"""
import fs from 'node:fs';
import { makeRunner } from %(runner)s;
const jobs = JSON.parse(fs.readFileSync(%(jobs)s, 'utf8'));
const runner = makeRunner({ pkgs: %(pkgs)s, root: %(root)s, jobs: 3 });
const out = await Promise.all(jobs.map(async (j) => {
  const r = await runner.grade(j.spec, j.src, 'tests');
  const first = r.rows.findIndex((x) => !x.ok);
  const row = first >= 0 ? r.rows[first] : null;
  return { ok: r.ok, key: r.key, error: r.error, detail: row ? String(row.error || row.got || row.actual || JSON.stringify(row)).split('\n').slice(-1)[0].slice(0, 110) : '' };
}));
await runner.close();
fs.writeFileSync(%(res)s, JSON.stringify(out));
"""


def part_b(pkgs):
    cache, jobs = {}, []
    def spec(f, k, i):
        if (f, k, i) not in cache:
            cache[(f, k, i)] = load(f)[k][i]['widget']
        return cache[(f, k, i)]
    # every changed code widget: solution passes, starter fails
    widgets = sorted({(c[0], c[1], c[2]) for c in CODINGS})
    for f, k, i in widgets:
        s = spec(f, k, i)
        jobs.append({'spec': s, 'src': s['solution'], 'tag': ('sol', f, k, i)})
        jobs.append({'spec': s, 'src': s['starter'], 'tag': ('start', f, k, i)})
    for f, k, i, line, want, label, src in CODINGS:
        jobs.append({'spec': spec(f, k, i), 'src': src, 'tag': ('coding', f, k, i, line, want, label)})
    with tempfile.TemporaryDirectory() as d:
        jp, rp, mp = os.path.join(d, 'jobs.json'), os.path.join(d, 'res.json'), os.path.join(d, 'run.mjs')
        json.dump(jobs, open(jp, 'w'))
        q = json.dumps
        open(mp, 'w').write(MJS % {'runner': q('file://' + os.path.join(ROOT, 'app', 'tools', 'code-runner.mjs')), 'jobs': q(jp), 'pkgs': q(os.path.abspath(pkgs)), 'root': q(os.path.join(ROOT, 'app')), 'res': q(rp)})
        subprocess.run(['node', mp], check=True)
        res = json.load(open(rp))
    for j, r in zip(jobs, res):
        t = j['tag']
        where = f'{t[1]} {t[2]}[{t[3]}]'
        if t[0] == 'sol':
            check(f'{where}: solution passes all {len(j["spec"]["tests"])} hidden tests', r['ok'], r['key'])
        elif t[0] == 'start':
            check(f'{where}: starter fails', not r['ok'], r['key'])
        else:
            want = None if t[5] == 0 else f'test-{t[5]}'
            check(f'{where} {t[4]}: {t[6]} -> {r["key"] or "passes"}', r['key'] == want, r['detail'])


if '--local-cdn' in sys.argv:
    part_b(sys.argv[sys.argv.index('--local-cdn') + 1])
else:
    print('     Part B skipped: give --local-cdn <pkgs>')

real = [b for b in bad if b not in KNOWN]
print(f'\n{len(bad)} failing check(s), {len(bad) - len(real)} of them recorded findings')
sys.exit(1 if real else 0)
