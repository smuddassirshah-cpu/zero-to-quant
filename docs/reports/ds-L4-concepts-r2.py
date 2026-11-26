"""Concept checks for ds level 4 (Trees and heaps), blind audit round 2 (ds-4-r2).

Run:   python docs/reports/ds-L4-concepts-r2.py            (concept checks only; exits 0 on correct content)
       python docs/reports/ds-L4-concepts-r2.py --sweep <pkgs>   (also runs Part 1 under the page's Pyodide 0.27.7)

Part 1 lists natural codings of every mistake a `feedback.byKey.test-N` line or a `mutants` entry names, with the
test each should fail first. Part 2 recomputes keys, slips, hidden-test expects and every empirical claim with its
own code (no content solution is reused, except where a check is about the model solution itself).
A check that fails because the content is wrong stays failing: see docs/reviews/audit-ds-4-r2.md.

Fix pass (Opus fixer): homework-4 item 2 gained hidden test 9 (heap peak at most one entry per list; NO_SORT is now test 10).
Re-pointed only where the old test list was encoded: "hw i1 expects" skips the peak test, which a new check covers; the H2
sweep now expects test-9 for the one-heap submission and the three new mutants, and test-10 for `sorted`.
"""

import json, sys, os

S_SUBS = []
def add(w, file, path, name, expect, src):
    S_SUBS.append(dict(w=w, file=file, path=path, name=name, expect=expect, src=src.lstrip("\n")))

def std(w, file, path, mutants):
    add(w, file, path, "solution", "PASS", "@solution")
    add(w, file, path, "starter", "", "@starter")
    for i, t in enumerate(mutants):
        add(w, file, path, f"mutant{i}", f"test-{t}", f"@mutant{i}")

LEVEL = """
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
PRE = """
def preorder(root):
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)
"""
INO = """
def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
"""
# ---- W1 l14 traversals
f, p, w = "l14-binary-trees.json", "screens[6].widget", "W1"
std(w, f, p, [1, 5])
add(w, f, p, "t2: inorder written as pre-order", "test-2", PRE + """
def inorder(root):
    if root is None:
        return []
    return [root.val] + inorder(root.left) + inorder(root.right)
""" + LEVEL)
add(w, f, p, "t2: inorder appends node first (shared list)", "test-2", PRE + """
def inorder(root):
    out = []
    def walk(n):
        if n is None:
            return
        out.append(n.val)
        walk(n.left)
        walk(n.right)
    walk(root)
    return out
""" + LEVEL)
add(w, f, p, "t7: level_order queue starts [root]", "test-7", PRE + INO + """
def level_order(root):
    out = []
    q = deque([root])
    while q:
        node = q.popleft()
        out.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return out
""")
add(w, f, p, "t7: level_order list queue, no None guard", "test-7", PRE + INO + """
def level_order(root):
    out, q = [], [root]
    i = 0
    while i < len(q):
        node = q[i]; i += 1
        out.append(node.val)
        for c in (node.left, node.right):
            if c is not None:
                q.append(c)
    return out
""")
add(w, f, p, "t5: preorder iterative stack, no None guard", "test-5", """
def preorder(root):
    out, st = [], [root]
    while st:
        n = st.pop()
        out.append(n.val)
        if n.right: st.append(n.right)
        if n.left: st.append(n.left)
    return out
""" + INO + LEVEL)
add(w, f, p, "t1: preorder no None case, loop version", "test-1", """
def preorder(root):
    out = [root.val]
    out += preorder(root.left)
    out += preorder(root.right)
    return out
""" + INO + LEVEL)

# ---- W2 l14 evaluate
f, p, w = "l14-binary-trees.json", "screens[10].widget", "W2"
std(w, f, p, [1, 4, 7, 8])
add(w, f, p, "t1: no leaf case, recurses below a leaf", "test-1", """
def evaluate(node):
    a = evaluate(node.left)
    b = evaluate(node.right)
    if node.val == '+': return a + b
    if node.val == '-': return a - b
    if node.val == '*': return a * b
    if node.val == 'max': return max(a, b)
    return node.val
""")
add(w, f, p, "t1: right minus left via operator dict", "test-1", """
def evaluate(node):
    if node.left is None and node.right is None:
        return node.val
    ops = {'+': lambda a, b: a + b, '-': lambda a, b: b - a, '*': lambda a, b: a * b, 'max': max}
    return ops[node.val](evaluate(node.left), evaluate(node.right))
""")
add(w, f, p, "t4: children-only leaf test, variant", "test-4", """
def evaluate(node):
    l, r = node.left, node.right
    a = l.val if l.left is None else evaluate(l)
    b = r.val if r.left is None else evaluate(r)
    if node.val == '+': return a + b
    if node.val == '-': return a - b
    if node.val == '*': return a * b
    return max(a, b)
""")
add(w, f, p, "x t7: '-' as abs difference", "", """
def evaluate(node):
    if node.left is None and node.right is None:
        return node.val
    a, b = evaluate(node.left), evaluate(node.right)
    if node.val == '+': return a + b
    if node.val == '-': return abs(a - b)
    if node.val == '*': return a * b
    return max(a, b)
""")
add(w, f, p, "t8: leaf told by not-a-str digit check", "test-8", """
def evaluate(node):
    if str(node.val).lstrip('-').isdigit():
        return node.val
    a, b = evaluate(node.left), evaluate(node.right)
    if node.val == '+': return a + b
    if node.val == '-': return a - b
    if node.val == '*': return a * b
    return max(a, b)
""")
add(w, f, p, "t8: leaf told by type(...) is int", "test-8", """
def evaluate(node):
    if type(node.val) is int:
        return node.val
    a, b = evaluate(node.left), evaluate(node.right)
    if node.val == '+': return a + b
    if node.val == '-': return a - b
    if node.val == '*': return a * b
    return max(a, b)
""")

# ---- W3 l15 insert/contains/min
f, p, w = "l15-search-trees.json", "screens[5].widget", "W3"
INS = """
def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
    elif v > root.val:
        root.right = insert(root.right, v)
    return root
"""
CON = """
def contains(root, v):
    node = root
    while node is not None:
        if v == node.val:
            return True
        node = node.left if v < node.val else node.right
    return False
"""
MIN = """
def min_value(root):
    node = root
    while node.left is not None:
        node = node.left
    return node.val
"""
std(w, f, p, [1])
add(w, f, p, "t1: result of insert not assigned", "test-1", """
def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        insert(root.left, v)
    elif v > root.val:
        insert(root.right, v)
    return root
""" + CON + MIN)
add(w, f, p, "t1: insert returns the new node, not root", "test-1", """
def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
        return root.left
    elif v > root.val:
        root.right = insert(root.right, v)
        return root.right
    return root
""" + CON + MIN)
add(w, f, p, "x t6: contains recursive, no None case at all", "", INS + """
def contains(root, v):
    if v == root.val:
        return True
    if v < root.val:
        return contains(root.left, v)
    return contains(root.right, v)
""" + MIN)
add(w, f, p, "t6: contains checks child before stepping", "test-6", INS + """
def contains(root, v):
    node = root
    while True:
        if v == node.val:
            return True
        nxt = node.left if v < node.val else node.right
        if nxt is None:
            return False
        node = nxt
""" + MIN)
add(w, f, p, "t6: contains recursive with child guards", "test-6", INS + """
def contains(root, v):
    if v == root.val:
        return True
    if v < root.val:
        return root.left is not None and contains(root.left, v)
    return root.right is not None and contains(root.right, v)
""" + MIN)
add(w, f, p, "t8: min_value steps left once before looping", "test-8", INS + CON + """
def min_value(root):
    node = root.left
    while node.left is not None:
        node = node.left
    return node.val
""")
add(w, f, p, "t8: min_value recursive, no base", "test-8", INS + CON + """
def min_value(root):
    return min_value(root.left) if root.left.left is not None else root.left.val
""")
add(w, f, p, "x t8: min_value returns root.left.val", "", INS + CON + """
def min_value(root):
    return root.left.val
""")
add(w, f, p, "t9: equal values go right (else)", "test-9", """
def insert(root, v):
    if root is None:
        return Node(v)
    if v < root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root
""" + CON + MIN)
add(w, f, p, "t9: equal values go left (<=)", "test-9", """
def insert(root, v):
    if root is None:
        return Node(v)
    if v <= root.val:
        root.left = insert(root.left, v)
    else:
        root.right = insert(root.right, v)
    return root
""" + CON + MIN)

# ---- W4 l15 validate_bst
f, p, w = "l15-search-trees.json", "screens[7].widget", "W4"
std(w, f, p, [])
add(w, f, p, "t2: children-only check", "test-2", """
def validate_bst(root, lo=None, hi=None):
    if root is None:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return validate_bst(root.left) and validate_bst(root.right)
""")
add(w, f, p, "t4: no empty-tree case, children guarded", "test-4", """
def validate_bst(root, lo=None, hi=None):
    if lo is not None and root.val <= lo:
        return False
    if hi is not None and root.val >= hi:
        return False
    if root.left and not validate_bst(root.left, lo, root.val):
        return False
    if root.right and not validate_bst(root.right, root.val, hi):
        return False
    return True
""")
add(w, f, p, "t6: non-strict bounds", "test-6", """
def validate_bst(root, lo=None, hi=None):
    if root is None:
        return True
    if lo is not None and root.val < lo:
        return False
    if hi is not None and root.val > hi:
        return False
    return validate_bst(root.left, lo, root.val) and validate_bst(root.right, root.val, hi)
""")
add(w, f, p, "t6: in-order equals sorted()", "test-6", """
def validate_bst(root, lo=None, hi=None):
    out = []
    def walk(n):
        if n:
            walk(n.left); out.append(n.val); walk(n.right)
    walk(root)
    return out == sorted(out)
""")
add(w, f, p, "t14: bounds +-2**31-1 as sentinels", "test-14", """
def validate_bst(root, lo=-2147483647, hi=2147483647):
    if root is None:
        return True
    if not (lo < root.val < hi):
        return False
    return validate_bst(root.left, lo, root.val) and validate_bst(root.right, root.val, hi)
""")
add(w, f, p, "t14: bounds +-10**9", "test-14", """
def validate_bst(root, lo=-10**9, hi=10**9):
    if root is None:
        return True
    if not (lo < root.val < hi):
        return False
    return validate_bst(root.left, lo, root.val) and validate_bst(root.right, root.val, hi)
""")
add(w, f, p, "ok: float inf bounds", "PASS", """
def validate_bst(root, lo=float('-inf'), hi=float('inf')):
    if root is None:
        return True
    if not (lo < root.val < hi):
        return False
    return validate_bst(root.left, lo, root.val) and validate_bst(root.right, root.val, hi)
""")

# ---- W5 l15 levels_between
f, p, w = "l15-search-trees.json", "screens[9].widget", "W5"
std(w, f, p, [7])
add(w, f, p, "t9: full in-order then filter", "test-9", """
def levels_between(root, lo, hi):
    out = []
    def walk(n):
        if n is None:
            return
        walk(n.left)
        if lo <= n.val <= hi:
            out.append(n.val)
        walk(n.right)
    walk(root)
    return out
""")
add(w, f, p, "t9: prunes the right side only", "test-9", """
def levels_between(root, lo, hi):
    out = []
    def walk(n):
        if n is None:
            return
        walk(n.left)
        if lo <= n.val <= hi:
            out.append(n.val)
        if n.val < hi:
            walk(n.right)
    walk(root)
    return out
""")
add(w, f, p, "t9: prunes the left side only", "test-9", """
def levels_between(root, lo, hi):
    out = []
    def walk(n):
        if n is None:
            return
        if n.val > lo:
            walk(n.left)
        if lo <= n.val <= hi:
            out.append(n.val)
        walk(n.right)
    walk(root)
    return out
""")
add(w, f, p, "t2: returns None when nothing found", "test-2", """
def levels_between(root, lo, hi):
    out = []
    def walk(n):
        if n is None:
            return
        if n.val > lo:
            walk(n.left)
        if lo <= n.val <= hi:
            out.append(n.val)
        if n.val < hi:
            walk(n.right)
    walk(root)
    if out:
        return out
""")
add(w, f, p, "t7: leaf shortcut on missing left, variant", "test-7", """
def levels_between(root, lo, hi):
    if root is None:
        return []
    if root.left is None:
        return [root.val] if lo <= root.val <= hi else []
    out = []
    if root.val > lo:
        out += levels_between(root.left, lo, hi)
    if lo <= root.val <= hi:
        out.append(root.val)
    if root.val < hi:
        out += levels_between(root.right, lo, hi)
    return out
""")

# ---- W6 l16 height/size
f, p, w = "l16-tree-recursion.json", "screens[4].widget", "W6"
std(w, f, p, [2, 4, 5])
SIZE = """
def size(root):
    if root is None:
        return 0
    return 1 + size(root.left) + size(root.right)
"""
add(w, f, p, "t1: height(None) is 0 (counts nodes)", "test-1", """
def height(root):
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))
""" + SIZE)
add(w, f, p, "t1: height has no None case, children guarded", "test-1", """
def height(root):
    h = 0
    if root.left:
        h = max(h, 1 + height(root.left))
    if root.right:
        h = max(h, 1 + height(root.right))
    return h
""" + SIZE)
add(w, f, p, "t2: None 0 and leaf 0 mixed", "test-2", """
def height(root):
    if root is None:
        return -1
    if root.left is None and root.right is None:
        return 1
    return 1 + max(height(root.left), height(root.right))
""" + SIZE)
add(w, f, p, "t4: size forgets the right side", "test-4", """
def height(root):
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))

def size(root):
    if root is None:
        return 0
    return 1 + size(root.left)
""")

# ---- W7 l16 is_balanced
f, p, w = "l16-tree-recursion.json", "screens[6].widget", "W7"
std(w, f, p, [13, 13, 13, 13])
H = """
def _h(n):
    if n is None:
        return -1
    return 1 + max(_h(n.left), _h(n.right))
"""
add(w, f, p, "t1: no empty-tree case", "test-1", H + """
def is_balanced(root):
    if abs(_h(root.left) - _h(root.right)) > 1:
        return False
    return (root.left is None or is_balanced(root.left)) and (root.right is None or is_balanced(root.right))
""")
add(w, f, p, "t5: root-only check", "test-5", H + """
def is_balanced(root):
    if root is None:
        return True
    return abs(_h(root.left) - _h(root.right)) <= 1
""")
add(w, f, p, "t5: root-only, heights in nodes", "test-5", """
def is_balanced(root):
    def h(n):
        return 0 if n is None else 1 + max(h(n.left), h(n.right))
    return root is None or abs(h(root.left) - h(root.right)) <= 1
""")
add(w, f, p, "t10: height at every node (the trap screen)", "test-10", H + """
def is_balanced(root):
    if root is None:
        return True
    return is_balanced(root.left) and is_balanced(root.right) and abs(_h(root.left) - _h(root.right)) <= 1
""")
add(w, f, p, "t10: height first then recurse", "test-10", H + """
def is_balanced(root):
    if root is None:
        return True
    if abs(_h(root.left) - _h(root.right)) > 1:
        return False
    return is_balanced(root.left) and is_balanced(root.right)
""")
add(w, f, p, "t13: -1 for None and -1 as flag (mixed)", "", """
def is_balanced(root):
    def check(node):
        if node is None:
            return -1
        lh = check(node.left)
        rh = check(node.right)
        if abs(lh - rh) > 1:
            return -2
        return 1 + max(lh, rh)
    return check(root) != -2
""")
add(w, f, p, "ok: tuple (height, ok)", "PASS", """
def is_balanced(root):
    def check(n):
        if n is None:
            return -1, True
        lh, lo = check(n.left)
        rh, ro = check(n.right)
        return 1 + max(lh, rh), lo and ro and abs(lh - rh) <= 1
    return check(root)[1]
""")

# ---- W8 l16 max_root_to_leaf
f, p, w = "l16-tree-recursion.json", "screens[9].widget", "W8"
std(w, f, p, [4, 4])
add(w, f, p, "t1: greedy, larger child each step", "test-1", """
def max_root_to_leaf(root):
    total, node = 0, root
    while node is not None:
        total += node.val
        kids = [c for c in (node.left, node.right) if c is not None]
        node = max(kids, key=lambda c: c.val) if kids else None
    return total
""")
add(w, f, p, "t1: greedy recursive", "test-1", """
def max_root_to_leaf(root):
    if root.left is None and root.right is None:
        return root.val
    if root.left is None:
        return root.val + max_root_to_leaf(root.right)
    if root.right is None:
        return root.val + max_root_to_leaf(root.left)
    nxt = root.left if root.left.val > root.right.val else root.right
    return root.val + max_root_to_leaf(nxt)
""")
add(w, f, p, "t4: missing child as -inf (correct idea)", "PASS", """
def max_root_to_leaf(root):
    def go(n):
        if n is None:
            return float('-inf')
        if n.left is None and n.right is None:
            return n.val
        return n.val + max(go(n.left), go(n.right))
    return go(root)
""")

# ---- W9 l17 push/pop
f, p, w = "l17-always-the-smallest.json", "screens[5].widget", "W9"
std(w, f, p, [5])
PUSH = """
def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent
"""
POP = """
def pop(heap):
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i, n = 0, len(heap)
        while True:
            smallest = i
            for c in (2 * i + 1, 2 * i + 2):
                if c < n and heap[c] < heap[smallest]:
                    smallest = c
            if smallest == i:
                break
            heap[i], heap[smallest] = heap[smallest], heap[i]
            i = smallest
    return top
"""
add(w, f, p, "t1: push swaps once (if, not while)", "test-1", """
def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    parent = (i - 1) // 2
    if i > 0 and heap[parent] > heap[i]:
        heap[i], heap[parent] = heap[parent], heap[i]
""" + POP)
add(w, f, p, "x t1: push parent index i // 2", "", """
def push(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0:
        parent = i // 2
        if heap[parent] <= heap[i]:
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent
""" + POP)
add(w, f, p, "t4: pop swaps with first (left) child", "test-4", PUSH + """
def pop(heap):
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i, n = 0, len(heap)
        while 2 * i + 1 < n:
            c = 2 * i + 1
            if heap[c] >= heap[i]:
                break
            heap[i], heap[c] = heap[c], heap[i]
            i = c
    return top
""")
add(w, f, p, "t4: pop swaps with first child that is smaller", "test-4", PUSH + """
def pop(heap):
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i, n = 0, len(heap)
        while True:
            moved = False
            for c in (2 * i + 1, 2 * i + 2):
                if c < n and heap[c] < heap[i]:
                    heap[i], heap[c] = heap[c], heap[i]
                    i = c
                    moved = True
                    break
            if not moved:
                break
    return top
""")
add(w, f, p, "t5?: right child read without a bounds check", "", PUSH + """
def pop(heap):
    top = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        i, n = 0, len(heap)
        while 2 * i + 1 < n:
            l, r = 2 * i + 1, 2 * i + 2
            c = l if heap[l] < heap[r] else r
            if heap[c] >= heap[i]:
                break
            heap[i], heap[c] = heap[c], heap[i]
            i = c
    return top
""")
add(w, f, p, "t5: pop writes heap[0] after emptying, variant", "test-5", PUSH + """
def pop(heap):
    heap[0], heap[-1] = heap[-1], heap[0]
    top = heap.pop()
    i, n = 0, len(heap)
    x = heap[0]
    while True:
        smallest = i
        for c in (2 * i + 1, 2 * i + 2):
            if c < n and heap[c] < heap[smallest]:
                smallest = c
        if smallest == i:
            break
        heap[i], heap[smallest] = heap[smallest], heap[i]
        i = smallest
    return top
""")
add(w, f, p, "t11: uses heapq", "test-11", """
import heapq
def push(heap, x):
    heapq.heappush(heap, x)

def pop(heap):
    return heapq.heappop(heap)
""")
add(w, f, p, "x: pop = min + remove (no heap)", "", PUSH + """
def pop(heap):
    m = min(heap)
    heap.remove(m)
    return m
""")

# ---- W10 l17 top_k
f, p, w = "l17-always-the-smallest.json", "screens[9].widget", "W10"
std(w, f, p, [4])
add(w, f, p, "t1: negated values, pop when over k", "test-1", """
import heapq
def top_k(xs, k):
    h = []
    for x in xs:
        heapq.heappush(h, -x)
        if len(h) > k:
            heapq.heappop(h)
    return sorted((-v for v in h), reverse=True)
""")
add(w, f, p, "t3: no k<=0 guard (solution shape)", "test-3", """
import heapq
def top_k(xs, k):
    h = []
    for x in xs:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)
    return sorted(h, reverse=True)
""")
add(w, f, p, "ok?: push then pop when over k, no guard", "PASS", """
import heapq
def top_k(xs, k):
    h = []
    for x in xs:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return sorted(h, reverse=True)
""")
add(w, f, p, "t4: skips a value already in the heap", "test-4", """
import heapq
def top_k(xs, k):
    if k <= 0:
        return []
    h = []
    for x in xs:
        if x in h:
            continue
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)
    return sorted(h, reverse=True)
""")
add(w, f, p, "t10: indexes xs with range(len(xs))", "test-10", """
import heapq
def top_k(xs, k):
    if k <= 0:
        return []
    h = []
    for i in range(len(xs)):
        x = xs[i]
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:
            heapq.heapreplace(h, x)
    return sorted(h, reverse=True)
""")
add(w, f, p, "t10: slices xs[:k] then the rest", "test-10", """
import heapq
def top_k(xs, k):
    if k <= 0:
        return []
    h = xs[:k]
    heapq.heapify(h)
    for x in xs[k:]:
        if x > h[0]:
            heapq.heapreplace(h, x)
    return sorted(h, reverse=True)
""")
add(w, f, p, "t11: sorts everything", "test-11", """
import heapq
def top_k(xs, k):
    if k <= 0:
        return []
    return sorted(xs, reverse=True)[:k]
""")
add(w, f, p, "ok: heapq.nlargest", "PASS", """
import heapq
def top_k(xs, k):
    return heapq.nlargest(k, xs)
""")

# ---- W11 l18 OrderBook
f, p, w = "l18-order-book-heaps.json", "screens[9].widget", "W11"
std(w, f, p, [13, 13, 13])
BOOK = """
import heapq
class OrderBook:
    def __init__(self):
        self.bids, self.asks, self.live = [], [], {}
        self.time = 0
    def add(self, order_id, side, price, qty):
        self.time += 1
        self.live[order_id] = [side, price, qty, self.time]
        if side == "buy":
            heapq.heappush(self.bids, (-price, %(T)s, order_id))
        else:
            heapq.heappush(self.asks, (price, %(T)s, order_id))
    def cancel(self, order_id):
        self.live.pop(order_id, None)
    def _top(self, heap):
        while heap and heap[0][2] not in self.live:
            heapq.heappop(heap)
        return heap[0] if heap else None
    def best_bid(self):
        %(BB)s
    def best_ask(self):
        %(BA)s
    def match(self):
        fills = []
        while True:
            b, a = %(TOPS)s
            if b is None or a is None or -b[0] < a[0]:
                return fills
            buy, sell = self.live[b[2]], self.live[a[2]]
            price = %(PRICE)s
            qty = min(buy[2], sell[2])
            fills.append((b[2], a[2], price, qty))
            buy[2] -= qty
            sell[2] -= qty
            if buy[2] == 0:
                del self.live[b[2]]
                %(POPB)s
            if sell[2] == 0:
                del self.live[a[2]]
                %(POPA)s
"""
D = dict(T="self.time",
         BB="t = self._top(self.bids)\n        return None if t is None else -t[0]",
         BA="t = self._top(self.asks)\n        return None if t is None else t[0]",
         TOPS="self._top(self.bids), self._top(self.asks)",
         PRICE="buy[1] if buy[3] < sell[3] else sell[1]", POPB="pass", POPA="pass")
def book(**kw):
    d = dict(D); d.update(kw); return BOOK % d
add(w, f, p, "ok: my own rewrite of the model", "PASS", book())
add(w, f, p, "t1: quotes read heap[0] with no empty check", "test-1",
    book(BB="return -self._top(self.bids)[0]", BA="return self._top(self.asks)[0]"))
add(w, f, p, "t3: quotes do not skip dead entries", "test-3",
    book(BB="return -self.bids[0][0] if self.bids else None", BA="return self.asks[0][0] if self.asks else None"))
add(w, f, p, "t5: time negated in the tuple", "test-5", book(T="-self.time"))
add(w, f, p, "t5: qty second in the tuple (larger first)", "", book(T="-qty"))
add(w, f, p, "t6: always the sell (ask) price", "test-6", book(PRICE="sell[1]"))
add(w, f, p, "t6?: always the buy price", "", book(PRICE="buy[1]"))
add(w, f, p, "t6?: midpoint", "", book(PRICE="(buy[1] + sell[1]) / 2"))
add(w, f, p, "t7: match pops filled entries itself, never skips cancelled", "test-7",
    book(TOPS="(self.bids[0] if self.bids else None), (self.asks[0] if self.asks else None)",
         POPB="heapq.heappop(self.bids)", POPA="heapq.heappop(self.asks)"))
add(w, f, p, "x: match trades only once per call", "", book().replace("        while True:\n            b, a", "        for _ in range(1):\n            b, a").replace("                return fills\n", "                return fills\n") + "        return fills\n")

# ---- W12 hw kth_smallest
f, p, w = "homework-4.json", "items[0].widget", "H1"
std(w, f, p, [])
add(w, f, p, "t8: full in-order list then index", "test-8", """
def kth_smallest(root, k):
    out = []
    def walk(n):
        if n is None:
            return
        walk(n.left); out.append(n.val); walk(n.right)
    walk(root)
    return out[k - 1]
""")
add(w, f, p, "t8: recursion counts but never stops", "test-8", """
def kth_smallest(root, k):
    state = [k, None]
    def walk(n):
        if n is None:
            return
        walk(n.left)
        state[0] -= 1
        if state[0] == 0:
            state[1] = n.val
        walk(n.right)
    walk(root)
    return state[1]
""")
add(w, f, p, "ok: recursive early exit", "PASS", """
def kth_smallest(root, k):
    state = [k, None]
    def walk(n):
        if n is None or state[0] <= 0:
            return
        walk(n.left)
        if state[0] <= 0:
            return
        state[0] -= 1
        if state[0] == 0:
            state[1] = n.val
            return
        walk(n.right)
    walk(root)
    return state[1]
""")
add(w, f, p, "x: k counted from 0", "", """
def kth_smallest(root, k):
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if k == 0:
            return node.val
        k -= 1
        node = node.right
""")

# ---- W13 hw merge_k
f, p, w = "homework-4.json", "items[1].widget", "H2"
std(w, f, p, [9, 9, 9])   # fix pass: three one-heap mutants on the new test 9
add(w, f, p, "t3: pushes xs[0] with no empty check", "test-3", """
import heapq
def merge_k(lists):
    heap = []
    for i, xs in enumerate(lists):
        heapq.heappush(heap, (xs[0], i, 0))
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out
""")
add(w, f, p, "t4: drops a value equal to the last output", "test-4", """
import heapq
def merge_k(lists):
    heap = []
    for i, xs in enumerate(lists):
        if xs:
            heapq.heappush(heap, (xs[0], i, 0))
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        if not out or out[-1] != value:
            out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out
""")
add(w, f, p, "t4?: (value, iterator) entries: TypeError on a tie", "", """
import heapq
def merge_k(lists):
    heap = []
    for xs in lists:
        it = iter(xs)
        for v in it:
            heapq.heappush(heap, (v, it))
            break
    out = []
    while heap:
        value, it = heapq.heappop(heap)
        out.append(value)
        for v in it:
            heapq.heappush(heap, (v, it))
            break
    return out
""")
add(w, f, p, "x: every item into one heap (not one entry per list)", "test-9", """
import heapq
def merge_k(lists):
    heap = []
    for xs in lists:
        for v in xs:
            heapq.heappush(heap, v)
    return [heapq.heappop(heap) for _ in range(len(heap))]
""")
add(w, f, p, "x: repeated min over list heads, no heap", "", """
def merge_k(lists):
    pos = [0] * len(lists)
    out = []
    while True:
        best = None
        for i, xs in enumerate(lists):
            if pos[i] < len(xs) and (best is None or xs[pos[i]] < lists[best][pos[best]]):
                best = i
        if best is None:
            return out
        out.append(lists[best][pos[best]])
        pos[best] += 1
""")
add(w, f, p, "ok: heapq.merge", "PASS", """
import heapq
def merge_k(lists):
    return list(heapq.merge(*lists))
""")
add(w, f, p, "t10: sorted(sum)", "test-10", """
import heapq
def merge_k(lists):
    return sorted(x for xs in lists for x in xs)
""")

# ---- W14 hw running_median
f, p, w = "homework-4.json", "items[2].widget", "H3"
std(w, f, p, [1, 7])
add(w, f, p, "t1: even count takes the lower top only", "test-1", """
import heapq
def running_median(xs):
    lo, hi, out = [], [], []
    for x in xs:
        if lo and x > -lo[0]:
            heapq.heappush(hi, x)
        else:
            heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        out.append(float(-lo[0]))
    return out
""")
add(w, f, p, "t1: even case adds both tops without negating lo", "test-1", """
import heapq
def running_median(xs):
    lo, hi, out = [], [], []
    for x in xs:
        if lo and x > -lo[0]:
            heapq.heappush(hi, x)
        else:
            heapq.heappush(lo, -x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) > len(hi):
            out.append(float(-lo[0]))
        else:
            out.append((lo[0] + hi[0]) / 2)
    return out
""")
add(w, f, p, "x: no rebalance", "", """
import heapq
def running_median(xs):
    lo, hi, out = [], [], []
    for x in xs:
        if lo and x > -lo[0]:
            heapq.heappush(hi, x)
        else:
            heapq.heappush(lo, -x)
        if len(lo) > len(hi):
            out.append(float(-lo[0]))
        elif len(lo) == len(hi):
            out.append((-lo[0] + hi[0]) / 2)
        else:
            out.append(float(hi[0]))
    return out
""")
add(w, f, p, "x: re-sort every step (no heaps)", "", """
def running_median(xs):
    seen, out = [], []
    for x in xs:
        seen.append(x)
        s = sorted(seen)
        n = len(s)
        out.append(float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)
    return out
""")

# ---- W15 hw save/load
f, p, w = "homework-4.json", "items[7].widget", "H8"
std(w, f, p, [])
SAVE = """
def save_tree(root):
    out = []
    def walk(node):
        if node is None:
            out.append("#")
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)
    walk(root)
    return ",".join(out)
"""
LOAD = """
def load_tree(text):
    tokens = iter(text.split(","))
    def read():
        tok = next(tokens)
        if tok == "#":
            return None
        node = Node(int(tok))
        node.left = read()
        node.right = read()
        return node
    return read()
"""
add(w, f, p, "t2: empty tree saved as ''", "test-2", """
def save_tree(root):
    if root is None:
        return ''
    out = []
    def walk(node):
        if node is None:
            out.append("#")
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)
    walk(root)
    return ",".join(out)
""" + LOAD)
add(w, f, p, "t3: reading position kept in a global", "test-3", SAVE + """
_pos = 0
def load_tree(text):
    global _pos
    toks = text.split(",")
    tok = toks[_pos]
    _pos += 1
    if tok == "#":
        return None
    node = Node(int(tok))
    node.left = load_tree(text)
    node.right = load_tree(text)
    return node
""")
add(w, f, p, "t3: values left as str", "test-3", SAVE + LOAD.replace("Node(int(tok))", "Node(tok)"))
add(w, f, p, "t5: reads one character per token", "test-5", SAVE + """
def load_tree(text):
    chars = iter(text.replace(",", ""))
    def read():
        c = next(chars)
        if c == "#":
            return None
        node = Node(int(c))
        node.left = read()
        node.right = read()
        return node
    return read()
""")
add(w, f, p, "t5: isdigit decides value or empty", "test-5", SAVE + """
def load_tree(text):
    tokens = iter(text.split(","))
    def read():
        tok = next(tokens)
        if not tok.isdigit():
            return None
        node = Node(int(tok))
        node.left = read()
        node.right = read()
        return node
    return read()
""")
add(w, f, p, "x: save treats 0 as empty", "", SAVE.replace("if node is None:", "if node is None or not node.val:") + LOAD)
add(w, f, p, "x: save omits # for leaves' children... level-order save", "", """
def save_tree(root):
    return ",".join("#" if v is None else str(v) for v in to_list(root)) or "#"
""" + LOAD)



# =====================================================================================
# Part 2. Concept checks. Each check is independent of the content's own solutions.
# =====================================================================================
import bisect, heapq, math, random, statistics, subprocess, tempfile
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
DS = os.path.join(HERE, "..", "..", "app", "content", "courses", "ds")
APP = os.path.join(HERE, "..", "..", "app")
sys.setrecursionlimit(20000)
random.seed(20261126)
FAIL, PASS = [], [0]

def check(name, cond, detail=""):
    if cond:
        PASS[0] += 1
    else:
        FAIL.append(name)
        print(f"FAIL  {name}  {detail}")

def X(t):
    e = t["expect"]
    return eval(e) if isinstance(e, str) else e

def load(name):
    return json.load(open(os.path.join(DS, name + ".json")))

L14, L15, L16, L17, L18 = (load(n) for n in ("l14-binary-trees", "l15-search-trees", "l16-tree-recursion",
                                              "l17-always-the-smallest", "l18-order-book-heaps"))
REV, HW = load("review-4"), load("homework-4")

class N:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def build(values):
    if not values or values[0] is None:
        return None
    it = iter(values); root = N(next(it)); q = deque([root])
    while q:
        node = q.popleft()
        for side in ("left", "right"):
            try: v = next(it)
            except StopIteration: return root
            if v is not None:
                c = N(v); setattr(node, side, c); q.append(c)
    return root

def from_canvas(params):
    """The canvas tree (rootLabel, nodes[..children]) as N; a child labelled ∅ is None."""
    def mk(d):
        if d is None or d.get("label") == "∅": return None
        kids = d.get("children") or []
        return N(d["label"], mk(kids[0]) if len(kids) > 0 else None, mk(kids[1]) if len(kids) > 1 else None)
    kids = params.get("nodes") or []
    return N(params["rootLabel"], mk(kids[0]) if kids else None, mk(kids[1]) if len(kids) > 1 else None)

def pre(n): return [] if n is None else [n.val] + pre(n.left) + pre(n.right)
def ino(n): return [] if n is None else ino(n.left) + [n.val] + ino(n.right)
def post(n): return [] if n is None else post(n.left) + post(n.right) + [n.val]
def lvl(n):
    out, q = [], deque([n] if n else [])
    while q:
        x = q.popleft(); out.append(x.val)
        if x.left: q.append(x.left)
        if x.right: q.append(x.right)
    return out
def height(n): return -1 if n is None else 1 + max(height(n.left), height(n.right))
def size(n): return 0 if n is None else 1 + size(n.left) + size(n.right)
def num(x):
    try: return float(str(x).replace("−", "-"))
    except ValueError: return x
def numtree(n):
    if n is None: return None
    return N(num(n.val), numtree(n.left), numtree(n.right))

# ---------------- lesson 14 ----------------
S = L14["screens"]
T = from_canvas(S[2]["canvas"]["params"])
check("l14 s0 leaves", sorted(S[0]["widget"]["answer"]) == ["l-l", "l-r", "r-l", "r-r"] and [x.val for x in (T.left.left, T.left.right, T.right.left, T.right.right)] == list("DEFG"))
check("l14 s1 depth of G is 2 and height 2", S[1]["widget"]["answer"] == 2 and height(T) == 2 and T.right.right.val == "G")
check("l14 s2 pre-order key", S[2]["widget"]["order"] == pre(T))
check("l14 s3 in-order key", S[3]["widget"]["order"] == ino(T))
check("l14 s4 post-order key", S[4]["widget"]["order"] == post(T))
check("l14 s2 slip C is level order", lvl(T)[:3] == ["A", "B", "C"])
# s5: queue after C is taken out and its children added
q = deque([T]); taken = []
while True:
    x = q.popleft(); taken.append(x.val)
    q.extend(c for c in (x.left, x.right) if c)
    if x.val == "C": break
check("l14 s5 queue after C", [x.val for x in q] == list("DEFG") and taken == list("ABC"))
# s6 hidden-test expects recomputed
tests = S[6]["widget"]["tests"]
env = {"build": build, "preorder": pre, "inorder": ino, "level_order": lvl}
check("l14 s6 all 14 expects", all(eval(t["call"], env) == X(t) for t in tests) and len(tests) == 14)
# s7 trap: swapped calls; and the claim that sorting 'hides the bug on this tree'
def pre_mirror(n): return [] if n is None else [n.val] + pre_mirror(n.right) + pre_mirror(n.left)
check("l14 s7 swapped calls give A C G F B E D", pre_mirror(T) == list("ACGFBED"))
target = list("DBEAFCG")
check("l14 s7 target is the in-order", ino(T) == target)
# feedback.byKey.d says sorting 'hides the bug on this tree'. It would have to return the asked-for order here.
says_hides = "hides the bug on this tree" in S[7]["feedback"]["byKey"]["d"]
check("l14 s7 byKey.d: sorting does NOT give D B E A F C G on this tree, so nothing is hidden (finding 1)",
      not (says_hides and sorted(pre(T)) != target), f"sorted gives {''.join(sorted(pre(T)))}, asked {''.join(target)}")
# s8: '+' joins cost Theta(n^2) on a chain, one shared list Theta(n)  (empirical: count element copies)
def chain(n):
    root = node = N(0)
    for i in range(1, n):
        node.left = N(i); node = node.left
    return root
def copies_plus(n_):
    c = [0]
    def w(x):
        if x is None: return []
        a, b = w(x.left), w(x.right)
        c[0] += len(a) + 1 + len(b)
        return a + [x.val] + b
    w(n_); return c[0]
c1, c2 = copies_plus(chain(1000)), copies_plus(chain(2000))
check("l14 s8 '+' copies grow x4 when a chain doubles (quadratic)", 3.9 < c2 / c1 < 4.1, f"{c2 / c1:.3f}")
bal = build(list(range(1, 1024))); bal2 = build(list(range(1, 2048)))
check("l14 s8 '+' on a perfect tree is n log n, not quadratic", 2.0 < copies_plus(bal2) / copies_plus(bal) < 2.4)
# s9 expression tree
E = numtree(from_canvas(S[9]["canvas"]["params"]))
def ev(n, sub=lambda a, b: a - b):
    if n.left is None and n.right is None: return n.val
    a, b = ev(n.left, sub), ev(n.right, sub)
    return {"×": a * b, "*": a * b, "-": sub(a, b), "−": sub(a, b), "+": a + b, "max": max(a, b)}[n.val]
w = S[9]["widget"]; slips = {x["id"]: x["value"] for x in w["wrong"]}
check("l14 s9 key 388", ev(E) == 388 == w["answer"])
check("l14 s9 slips", slips == {"fee": 50 * (108 - 100), "sign": 12 - 400, "gross": 50 * 108 - 12})
tests = S[10]["widget"]["tests"]
check("l14 s10 expects", all(ev(build(eval(t["call"][len("evaluate(build("):-2]))) == X(t) for t in tests))
check("l14 s10 test 1 with right-minus-left is 412", ev(build(['-', '*', 12, 50, '-', None, None, None, None, 108, 100]), lambda a, b: b - a) == 412)
check("l14 s10 test 6 is a bull call spread worth 10", max(110 - 95, 0) - max(110 - 105, 0) == 10 == X(tests[5]))
check("l14 quiz0", ino(build([5, 4, None, 3])) == [3, 4, 5] and pre(build([5, 4, None, 3])) == [5, 4, 3])
check("l14 quiz3 one node has height 0", height(N(1)) == 0 == L14["quiz"][3]["widget"]["answer"])

# ---------------- lesson 15 ----------------
S = L15["screens"]
def bst_insert(root, v):
    if root is None: return N(v)
    if v < root.val: root.left = bst_insert(root.left, v)
    elif v > root.val: root.right = bst_insert(root.right, v)
    return root
def bst_from(vs):
    r = None
    for v in vs: r = bst_insert(r, v)
    return r
def path_to(root, v):
    """Region ids along the search path for v, ending where v is or would be."""
    ids, node, cur = [], root, ""
    while node is not None and node.val != v:
        step = "l" if v < node.val else "r"
        cur = step if not cur else cur + "-" + step
        ids.append(cur); node = node.left if step == "l" else node.right
    return ids, node
B = bst_from([50, 30, 70, 20, 40, 60, 80])
ids, hit = path_to(B, 60)
check("l15 s0 path to 60", ids == S[0]["widget"]["answer"] and hit is not None)
check("l15 s1 65 lands at r-l-r", path_to(B, 65)[0][-1] == S[1]["widget"]["answer"][0])
check("l15 s2 35 and 85", [path_to(B, 35)[0][-1], path_to(B, 85)[0][-1]] == S[2]["widget"]["answer"])
check("l15 s3 options are in/pre/level/post", [ino(B), pre(B), lvl(B), post(B)] == [eval(o["text"].strip("`")) for o in S[3]["widget"]["options"]])
C = bst_from([10, 20, 30, 40, 50])
check("l15 s4 sorted inserts: chain, height 4, 5 comparisons", height(C) == 4 and len(path_to(C, 50)[0]) + 1 == 5 == S[4]["widget"]["answer"])
check("l15 s4 slips", {x["id"]: x["value"] for x in S[4]["widget"]["wrong"]} == {"log": math.ceil(math.log2(5)), "edges": 4})
# in-order of a BST is sorted; floor(log2 n) <= h <= n-1 (Monte Carlo, 2,000 random insert orders)
ok_sorted = ok_bounds = True
for _ in range(2000):
    n = random.randint(1, 60); vs = random.sample(range(1000), n); r = bst_from(vs)
    ok_sorted &= ino(r) == sorted(vs)
    ok_bounds &= math.floor(math.log2(n)) <= height(r) <= n - 1
check("l15 in-order of a BST is sorted (2,000 random trees)", ok_sorted)
check("l15 s8 floor(log2 n) <= h <= n-1 (2,000 random trees)", ok_bounds)
check("l15 s8 both bounds are attained", height(bst_from(range(1, 41))) == 39 and height(build(list(range(1, 1024)))) == 9 == math.floor(math.log2(1023)))
check("l15 s8 1,023 perfect: 10 comparisons", 2 ** 10 - 1 == 1023 and S[8]["widget"]["answer"] == 10)
check("l15 quiz1 1,000 ascending: height 999", height(bst_from(range(1000))) == 999 == L15["quiz"][1]["widget"]["answer"])
# s5 expects through an independent insert
def to_list(root):
    out, q = [], deque([root])
    while q:
        x = q.popleft()
        if x is None: out.append(None); continue
        out.append(x.val); q.append(x.left); q.append(x.right)
    while out and out[-1] is None: out.pop()
    return out
def contains(r, v): return path_to(r, v)[1] is not None
def min_value(r): return ino(r)[0]
env = {"bst_from": bst_from, "to_list": to_list, "inorder": ino, "contains": contains, "min_value": min_value, "insert": bst_insert}
check("l15 s5 all 13 expects", all(eval(t["call"], env) == X(t) for t in S[5]["widget"]["tests"]) and len(S[5]["widget"]["tests"]) == 13)
# s6 trap: children-only check accepts a non-BST
def looks_ok(node):
    if node is None: return True
    if node.left and node.left.val >= node.val: return False
    if node.right and node.right.val <= node.val: return False
    return looks_ok(node.left) and looks_ok(node.right)
def valid(n, lo=-math.inf, hi=math.inf):
    return n is None or (lo < n.val < hi and valid(n.left, lo, n.val) and valid(n.right, n.val, hi))
trap = numtree(from_canvas(S[6]["canvas"]["params"]))
check("l15 s6 looks_ok is True on a tree that is not a BST, and a search for 6 misses", looks_ok(trap) and not valid(trap) and not contains(trap, 6) and 6 in pre(trap))
def balanced(vs):
    if not vs: return None
    m = len(vs) // 2
    return N(vs[m], balanced(vs[:m]), balanced(vs[m + 1:]))
env = {"build": build, "validate_bst": valid, "balanced": balanced}
check("l15 s7 all 14 expects", all(eval(t["call"], env) == X(t) for t in S[7]["widget"]["tests"]))
# s9: pruned range walk reads O(h + k) nodes; expects
def rng(root, lo, hi, seen):
    out = []
    def walk(n):
        if n is None: return
        seen.add(id(n))
        if n.val > lo: walk(n.left)
        if lo <= n.val <= hi: out.append(n.val)
        if n.val < hi: walk(n.right)
    walk(root); return out
big = balanced(list(range(1, 1024)))
worst = 0
for _ in range(3000):
    lo = random.randint(-5, 1030); k = random.randint(0, 5); seen = set()
    got = rng(big, lo, lo + k, seen)
    worst = max(worst, len(seen) - len(got))
check("l15 s9 pruned walk reads at most k + 2h nodes on 1,023 (3,000 random ranges)", worst <= 2 * 10, str(worst))
env = {"build": build, "balanced": balanced, "levels_between": lambda r, lo, hi: rng(r, lo, hi, set()),
       "touched": lambda r, lo, hi: (lambda s: (rng(r, lo, hi, s), len(s))[1])(set())}
check("l15 s9 all 11 expects", all(eval(t["call"], env) == X(t) for t in S[9]["widget"]["tests"]))
# quiz 3: sort() after each insert compares about n items; insort about log2 n  (count comparisons)
class Cnt:
    n = 0
    def __init__(self, v): self.v = v
    def __lt__(self, o): Cnt.n += 1; return self.v < o.v
xs = [Cnt(v) for v in range(0, 20000, 2)]
Cnt.n = 0; ys = xs + [Cnt(9999)]; ys.sort(); by_sort = Cnt.n
Cnt.n = 0; bisect.insort(xs, Cnt(9999)); by_bisect = Cnt.n
check("l15 quiz3 sort() of n sorted + 1 item compares about n; insort about log2 n", by_sort >= 9999 and by_bisect <= math.ceil(math.log2(10001)) + 1, f"{by_sort} vs {by_bisect}")
check("l15 quiz2 tick index", round((100.25 - 90.00) / 0.01) == 1025 and round((110.00 - 90.00) / 0.01) + 1 == 2001)

# ---------------- lesson 16 ----------------
S = L16["screens"]
T0 = numtree(from_canvas(S[0]["canvas"]["params"]))
check("l16 s0 height 3, slips 4 and 1", height(T0) == 3 == S[0]["widget"]["answer"] and height(T0.right) + 1 == 1)
rows = S[1]["widget"]["rows"]
check("l16 s1 table", [r[1]["answer"] if isinstance(r[1], dict) else num(r[1]) for r in rows] == [height(None), 0, height(T0.left.left), height(T0.left), height(T0)])
def best(n):
    if n.left is None and n.right is None: return n.val, [n.val]
    c = [best(k) for k in (n.left, n.right) if k is not None]
    v, p = max(c, key=lambda t: t[0])
    return n.val + v, [n.val] + p
R = numtree(from_canvas(S[2]["canvas"]["params"]))
check("l16 s2 best route 5,4,11,7 = 27; slips 26 and 22", best(R) == (27, [5, 4, 11, 7]) and 5 + 8 + 13 == 26 and 5 + 4 + 11 + 2 == 22 and best(R.right)[0] == 21 and best(R.left)[0] == 22)
def unbalanced_nodes(n, acc):
    if n is None: return
    if abs(height(n.left) - height(n.right)) > 1: acc.append(n.val)
    unbalanced_nodes(n.left, acc); unbalanced_nodes(n.right, acc)
U = numtree(from_canvas(S[3]["canvas"]["params"])); acc = []; unbalanced_nodes(U, acc)
check("l16 s3 only node 2 is lopsided; root gap is 1", acc == [2] and S[3]["widget"]["answer"] == ["l"] and abs(height(U.left) - height(U.right)) == 1)
env = {"build": build, "height": height, "size": size}
check("l16 s4 all 10 expects", all(eval(t["call"], env) == X(t) for t in S[4]["widget"]["tests"]))
# s5: the naive is_balanced walks n(n-1)/2 nodes on a chain (count the nodes its height calls visit)
def naive_visits(root):
    c = [0]
    def h(n):
        if n is None: return -1
        c[0] += 1
        return 1 + max(h(n.left), h(n.right))
    def isb(n):
        if n is None: return True
        a, b = isb(n.left), isb(n.right)
        gap = abs(h(n.left) - h(n.right))      # computed before the return, as on the screen: no short circuit
        return a and b and gap <= 1
    isb(root); return c[0]
check("l16 s5 chain of 1,000: exactly n(n-1)/2 = 499,500 node visits", naive_visits(chain(1000)) == 499500)
v1, v2 = naive_visits(build(list(range(1, 1024)))), naive_visits(build(list(range(1, 2048))))
check("l16 s5 balanced tree: about n log n (ratio near 2.2 when n doubles, not 4)", 2.0 < v2 / v1 < 2.5, f"{v2 / v1:.2f}")
def bal_ref(n):
    return n is None or (abs(height(n.left) - height(n.right)) <= 1 and bal_ref(n.left) and bal_ref(n.right))
def chain_tree(n):
    return chain(n)
env = {"build": build, "is_balanced": bal_ref, "chain": chain_tree, "reads_for": lambda v: 0}
check("l16 s6 all 13 expects", all(eval(t["call"], env) == X(t) for t in S[6]["widget"]["tests"]))
# s7 / quiz0 / diameter: brute force over random trees
def rand_tree(n):
    if n == 0: return None
    k = random.randint(0, n - 1)
    return N(random.randint(-9, 9), rand_tree(k), rand_tree(n - 1 - k))
def diameter_brute(root):
    adj, nodes = {}, []
    def w(n, p):
        if n is None: return
        nodes.append(n); adj.setdefault(id(n), [])
        if p is not None: adj[id(n)].append(p); adj[id(p)].append(n)
        w(n.left, n); w(n.right, n)
    w(root, None); bestd = 0
    for s in nodes:
        dist = {id(s): 0}; q = deque([s])
        while q:
            x = q.popleft()
            for y in adj[id(x)]:
                if id(y) not in dist: dist[id(y)] = dist[id(x)] + 1; q.append(y)
        bestd = max(bestd, max(dist.values()))
    return bestd
def diameter_formula(root):
    b = [0]
    def w(n):
        if n is None: return
        b[0] = max(b[0], height(n.left) + height(n.right) + 2); w(n.left); w(n.right)
    w(root); return b[0]
def bal_nodes(n):
    def h(x): return 0 if x is None else 1 + max(h(x.left), h(x.right))
    return n is None or (abs(h(n.left) - h(n.right)) <= 1 and bal_nodes(n.left) and bal_nodes(n.right))
okd = okc = okm = True
def route_none0(n): return 0 if n is None else n.val + max(route_none0(n.left), route_none0(n.right))
for _ in range(1500):
    t = rand_tree(random.randint(1, 25))
    okd &= diameter_brute(t) == diameter_formula(t)
    okc &= bal_ref(t) == bal_nodes(t)
check("l16 s7 diameter = max over v of h(L)+h(R)+2 (1,500 random trees against brute force)", okd)
check("l16 quiz0 the two height conventions give the same verdict (1,500 random trees)", okc)
check("l16 quiz2 diameter of build([1,2,3,4,5]) is 3", diameter_brute(build([1, 2, 3, 4, 5])) == 3 == L16["quiz"][2]["widget"]["answer"])
Lt = numtree(from_canvas(S[8]["canvas"]["params"]))
def greedy(n):
    tot = 0
    while n is not None:
        tot += n.val; kids = [k for k in (n.left, n.right) if k is not None]
        n = max(kids, key=lambda k: k.val) if kids else None
    return tot
check("l16 s8 lattice: best 8 along 2,3,-5,8; greedy 6; skip slip 13", best(Lt) == (8, [2, 3, -5, 8]) and greedy(Lt) == 6 and 2 + 3 + 8 == 13)
env = {"build": build, "max_root_to_leaf": lambda r: best(r)[0]}
check("l16 s9 all 10 expects", all(eval(t["call"], env) == X(t) for t in S[9]["widget"]["tests"]))
check("l16 s9 a missing child as 0 gives 1 on build([1,-5])", route_none0(build([1, -5])) == 1)

# ---------------- lesson 17 ----------------
S = L17["screens"]
H0 = [2, 5, 3, 9, 6, 7, 8]
def is_heap(h): return all(h[(i - 1) // 2] <= h[i] for i in range(1, len(h)))
check("l17 s0 list is a heap; children of index 1 at 3 and 4", is_heap(H0) and S[0]["widget"]["answer"] == ["c3", "c4"])
check("l17 s1 parent formula inverts the child formula for i < 10,000", all((2 * i + 1 - 1) // 2 == i == (2 * i + 2 - 1) // 2 for i in range(10000)))
def push(h, x):
    h.append(x); i = len(h) - 1; swaps = 0
    while i > 0 and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2; h[i], h[p] = h[p], h[i]; i = p; swaps += 1
    return swaps
h = list(H0); sw = push(h, 4); h2 = list(H0); heapq.heappush(h2, 4)
check("l17 s2 push 4: two swaps, [2,4,3,5,6,7,8,9], same as heapq", sw == 2 and h == [2, 4, 3, 5, 6, 7, 8, 9] == h2)
top = heapq.heappop(h2)
check("l17 s3 pop: 2 out, [3,4,7,5,6,9,8]", top == 2 and h2 == [3, 4, 7, 5, 6, 9, 8])
big = list(range(1, 1000001)); sw = push(big, 0)
check("l17 s4 a push onto 1,000,000 items makes at most 19 swaps (worst case run)", sw == 19 == S[4]["widget"]["answer"] and math.floor(math.log2(10 ** 6)) + 1 == 20)
check("l17 s4 levels = floor(log2 n) + 1 for n < 5,000", all(max(math.floor(math.log2(i + 1)) for i in range(n)) + 1 == math.floor(math.log2(n)) + 1 for n in range(1, 5000, 7)))
# s2 explain says 'at most as many swaps as the tree has levels': the tight bound is levels - 1 (finding)
check("l17 s2 tight bound on swaps is levels - 1", sw == 20 - 1)
# s6 trap
hh = []
for x in [120, 45, 300, 80, 210, 60]:
    heapq.heappush(hh, -x)
    if len(hh) > 3: heapq.heappop(hh)
check("l17 s6 negated heap keeps 45, 60, 80", sorted(-v for v in hh) == [45, 60, 80])
asks = []
for t in [(100.03, 1, "A1"), (100.02, 4, "A2"), (100.02, 2, "A3"), (100.05, 3, "A4")]: heapq.heappush(asks, t)
check("l17 s8 asks[0] is A3", asks[0][2] == "A3")
# heap claims by run: heapsort; top-k comparisons linear in n; re-sorting n^2 log n against heap n log n
ok = True
for _ in range(300):
    xs = [random.randint(0, 50) for _ in range(random.randint(0, 40))]; hq = list(xs); heapq.heapify(hq)
    ok &= [heapq.heappop(hq) for _ in range(len(xs))] == sorted(xs)
check("l17 s7 popping everything returns sorted order (300 runs)", ok)
def cmp_total(n, mode):
    data = [Cnt(random.random()) for _ in range(n)]; Cnt.n = 0; seen = []
    for x in data:
        if mode == "sort": seen.append(x); sorted(seen)[0]
        else: heapq.heappush(seen, x); seen[0]
    return Cnt.n
s1, s2 = cmp_total(600, "sort"), cmp_total(1200, "sort")
p1, p2 = cmp_total(20000, "heap"), cmp_total(40000, "heap")
check("l17 quiz3 re-sorting grows about x4.4 when n doubles (n^2 log n)", 4.0 < s2 / s1 < 4.8, f"{s2 / s1:.2f}")
check("l17 quiz3 heap pushes grow about x2 when n doubles (at most n log n)", 1.8 < p2 / p1 < 2.4, f"{p2 / p1:.2f}")
def topk_cmp(n, k):
    data = [Cnt(random.random()) for _ in range(n)]; Cnt.n = 0; hq = []
    for x in data:
        if len(hq) < k: heapq.heappush(hq, x)
        elif hq[0] < x: heapq.heapreplace(hq, x)
    return Cnt.n
check("l17 s7 top-10 of n: comparisons linear in n, far below n log2 n", topk_cmp(200000, 10) < 2.0 * 200000 and 1.8 < topk_cmp(200000, 10) / topk_cmp(100000, 10) < 2.2)
check("l17 quiz0 parent of 10 is 4; slips 5 and 21", (10 - 1) // 2 == 4 and 10 // 2 == 5 and 2 * 10 + 1 == 21)
# quiz1 option d: reverse-sorted list, then heappop twice: largest first, then the smallest (10,000 random lists)
ok = True
for _ in range(10000):
    xs = sorted(random.sample(range(10 ** 6), random.randint(2, 40)), reverse=True)
    a, b = heapq.heappop(xs), heapq.heappop(xs)
    ok &= (a == max([a, b] + xs)) and (b == min([b] + xs))
check("l17 quiz1 d: on a reverse-sorted list the first heappop is the largest and the next the smallest (10,000 runs)", ok)
env = {"top_k": lambda xs, k: sorted(xs, reverse=True)[:max(k, 0)], "peak_bytes": lambda f: 0}
check("l17 s9 all 11 expects", all(eval(t["call"], env) == X(t) for t in S[9]["widget"]["tests"]))
check("l17 s9 heapq.nlargest agrees with the model on repeats", heapq.nlargest(2, [7, 7, 3, 7, 1]) == [7, 7])

# ---------------- lesson 18 ----------------
S = L18["screens"]
class Naive:
    """Independent book: plain lists, sorted on every read. Price-time priority, fills at the resting price."""
    def __init__(self): self.o = {}; self.t = 0
    def add(self, i, side, price, qty): self.t += 1; self.o[i] = [side, price, qty, self.t]
    def cancel(self, i): self.o.pop(i, None)
    def _side(self, s): return sorted(((-p if s == "buy" else p, t, i) for i, (sd, p, q, t) in self.o.items() if sd == s))
    def best_bid(self): b = self._side("buy"); return self.o[b[0][2]][1] if b else None
    def best_ask(self): a = self._side("sell"); return self.o[a[0][2]][1] if a else None
    def match(self):
        fills = []
        while True:
            b, a = self._side("buy"), self._side("sell")
            if not b or not a: return fills
            bo, ao = self.o[b[0][2]], self.o[a[0][2]]
            if bo[1] < ao[1]: return fills
            q = min(bo[2], ao[2]); px = bo[1] if bo[3] < ao[3] else ao[1]
            fills.append((b[0][2], a[0][2], px, q)); bo[2] -= q; ao[2] -= q
            for i in (b[0][2], a[0][2]):
                if self.o[i][2] == 0: del self.o[i]
def play(events, cls=Naive):
    book, out = cls(), []
    for name, *args in events:
        r = getattr(book, name)(*args)
        if name in ("best_bid", "best_ask", "match"): out.append(r)
    return out
tests = S[9]["widget"]["tests"]; okb = True
for i, t in enumerate(tests):
    if i == 11:
        continue    # 8,000 orders: checked by arithmetic below (the naive book is quadratic)
    okb &= eval(t["call"], {"play": play}) == X(t)
check("l18 s9 expects of tests 1-11 and 13 against an independent naive book", okb)
# test 12 by arithmetic: 80 sells of 10 at each of 1001..1050; BIG buys 15,000 up to 1020
per_level = 4000 // 50 * 10; full, rest = divmod(15000, per_level)
check("l18 s9 test 12 expect (1500, 15000, 1000, 1019)", tuple(X(tests[11])) == (15000 // 10, 15000, 1000, 1001 + full) and rest > 0 and 20 * per_level >= 15000 and 50 % 3 != 0)
# s2 table through the naive book
bk = Naive()
for i, p in (("B1", 100.00), ("B2", 99.99), ("B3", 99.98)): bk.add(i, "buy", p, 100)
for i, p in (("A1", 100.02), ("A2", 100.03), ("A3", 100.05)): bk.add(i, "sell", p, 100)
got = []
for step in (lambda: bk.add("A4", "sell", 100.01, 100), lambda: bk.cancel("B1"), lambda: bk.add("B4", "buy", 100.00, 50), lambda: bk.cancel("A4")):
    step(); got.append([bk.best_bid(), bk.best_ask()])
check("l18 s2 quote table", got == [[r[1]["answer"], r[2]["answer"]] for r in S[2]["widget"]["rows"]])
r = play([("add", "A1", "sell", 100.02, 200), ("add", "A2", "sell", 100.03, 400), ("add", "A3", "sell", 100.05, 100), ("add", "B", "buy", 100.03, 500), ("match",)])[0]
check("l18 s3 100 left at 100.03; cost 50,013", 400 - r[1][3] == 100 == S[3]["widget"]["answer"] and round(sum(f[2] * f[3] for f in r), 2) == 50013.0)
r = play([("add", "A1", "sell", 100.02, 200), ("add", "A5", "sell", 100.02, 300), ("add", "B", "buy", 100.02, 250), ("match",)])[0]
check("l18 s4 fills 200 and 50", [f[3] for f in r] == [200, 50])
# s5: list.remove can break the heap rule; remove + heapify is right; lazy deletion pops each dead entry once
broke = 0
for _ in range(2000):
    hq = random.sample(range(1000), 12); heapq.heapify(hq); hq.remove(hq[random.randint(1, 11)]); broke += not is_heap(hq)
check("l18 s5 list.remove from the middle sometimes breaks the heap rule (2,000 runs)", broke > 0, str(broke))
# s5 hint 'A heap can only remove cheaply from the top' and summary 'Never delete from the middle of a heap' (finding 2):
# with the entry's index known, a middle delete is O(log n): move the last item in, then sift (CLRS ex. 6.5-10; Sedgewick 2.4 IndexMinPQ)
okdel, worst_cmp = True, 0
for _ in range(2000):
    hq = [Cnt(v) for v in random.sample(range(10 ** 6), 1023)]; heapq.heapify(hq)
    i = random.randint(1, len(hq) - 1); gone_v = hq[i].v; Cnt.n = 0
    last = hq.pop()
    if i < len(hq):
        hq[i] = last; heapq._siftup(hq, i); heapq._siftdown(hq, 0, i)
    worst_cmp = max(worst_cmp, Cnt.n)
    okdel &= all(not (hq[k] < hq[(k - 1) // 2]) for k in range(1, len(hq))) and gone_v not in [c.v for c in hq]
check("l18 s5 evidence: delete at a known index keeps the heap in O(log n) comparisons (2,000 runs on 1,023 items)", okdel and worst_cmp <= 4 * 10, str(worst_cmp))
src = S[9]["widget"]["solution"]; ns = {}; exec(src, ns); Model = ns["OrderBook"]
pops = {"dead": 0}; orig = heapq.heappop
ok_inv = True; cancels = adds = 0
book = Model(); cancelled = set(); ids = []
def counting_pop(hq):
    e = orig(hq)
    if e[2] in cancelled: pops["dead"] += 1
    return e
ns["heapq"] = type("HQ", (), {"heappush": staticmethod(heapq.heappush), "heappop": staticmethod(counting_pop)})
for step in range(60000):
    u = random.random()
    if u < 0.5 or not ids:
        i = f"o{step}"; side = random.choice(["buy", "sell"])
        book.add(i, side, 100 + random.randint(-6, 0) if side == "buy" else 101 + random.randint(0, 6), random.randint(1, 5) * 10); ids.append(i); adds += 1
    elif u < 0.95:
        i = ids.pop(random.randrange(len(ids)))
        if i in book.live: cancelled.add(i); cancels += 1
        book.cancel(i)
    else:
        book.best_bid(); book.best_ask()
check("l18 s7 reads pop at most one dead entry per cancel (60,000 random messages)", 0 < pops["dead"] <= cancels, f"{pops['dead']} of {cancels}")
check("l18 s7 key 900,000 and slips", S[7]["widget"]["answer"] == 900000 and [x["value"] for x in S[7]["widget"]["wrong"]] == [1000000, 900000 * 1000000])
# 'Filled ones are removed as they trade': after match() in the model, no filled entry is left at a top
book = Model(); gone = set(); okf = True
for step in range(4000):
    side = random.choice(["buy", "sell"]); book.add(f"x{step}", side, random.randint(95, 105), random.randint(1, 4) * 10)
    for f in book.match(): pass
    for hq in (book.bids, book.asks):
        okf &= all(e[2] in book.live for e in hq)
check("l18 s7 slip 'adds': in the model every filled entry is popped inside the same match call", okf)
# the same model and the naive book agree on random message streams (price-time priority, resting price)
def stream(n):
    ev, live = [], []
    for s in range(n):
        u = random.random()
        if u < 0.55 or not live:
            i = f"k{s}"; live.append(i); ev.append(("add", i, random.choice(["buy", "sell"]), random.randint(98, 102), random.randint(1, 5) * 10))
        elif u < 0.75: ev.append(("cancel", live.pop(random.randrange(len(live)))))
        elif u < 0.9: ev.append(("match",))
        else: ev.append((random.choice(["best_bid", "best_ask"]),))
    return ev
ns["heapq"] = heapq
okm = all((lambda e: play(e, Model) == play(e, Naive))(stream(120)) for _ in range(300))
check("l18 s9 model solution equals the naive book on 300 random streams", okm)

# ---------------- review 4 ----------------
I = REV["items"]
t = numtree(from_canvas(I[0]["canvas"]["params"]))
opts = [[int(x) for x in o["text"].split(", ")] for o in I[0]["widget"]["options"]]
check("rev i0 post / pre / in-order", opts[:3] == [post(t), pre(t), ino(t)])
t = numtree(from_canvas(I[2]["canvas"]["params"]))
check("rev i2 height 3", height(t) == 3 == I[2]["widget"]["answer"])
h = [3, 5, 4, 9, 6]; push(h, 1)
check("rev i3 push 1", str(h) == I[3]["widget"]["options"][0]["text"].strip("`"))
check("rev i4 spread 0.04 and slips", round(100.03 - 99.99, 2) == I[4]["widget"]["answer"] and [x["value"] for x in I[4]["widget"]["wrong"]] == [round(100.01 - 100.00, 2), round(100.03 - 99.98, 2)])
lists = [eval(o["text"].strip("`")) for o in I[5]["widget"]["options"]]
check("rev i5 only the first list is a strict BST", [valid(build(x)) for x in lists] == [True, False, False, False])
def valid_clrs(n, lo=-math.inf, hi=math.inf):   # CLRS 12.1: left keys <= node <= right keys
    return n is None or (lo <= n.val <= hi and valid_clrs(n.left, lo, n.val) and valid_clrs(n.right, n.val, hi))
# finding: under the CLRS convention (equal keys allowed) option d is a search tree too, and the item states no convention
states_rule = any(wd in I[5]["prose"] for wd in ("strict", "repeat", "duplicate", "distinct"))
check("rev i5 option d is wrong under every valid convention, or the item states its convention (finding 4)",
      states_rule or not valid_clrs(build(lists[3])), "valid under CLRS 12.1 (<=) and no convention in the prose")
check("rev i7 59,995 and slips", round(200 * 100.00 + 300 * 99.99 + 100 * 99.98, 2) == I[7]["widget"]["answer"] and [x["value"] for x in I[7]["widget"]["wrong"]] == [round(600 * 99.98), 600 * 100])
t = numtree(from_canvas(I[8]["canvas"]["params"]))
check("rev i8 diameter 4; through the root 3", diameter_brute(t) == 4 == I[8]["widget"]["answer"] and height(t.left) + height(t.right) + 2 == 3)

# ---------------- homework 4 ----------------
I = HW["items"]
env = {"build": build, "balanced": balanced, "kth_smallest": lambda r, k: ino(r)[k - 1], "touched": lambda r, k: 0}
check("hw i0 expects", all(eval(t["call"], env) == X(t) for t in I[0]["widget"]["tests"]))
env = {"merge_k": lambda ls: sorted(x for l in ls for x in l), "NO_SORT": True}
check("hw i1 expects", all(eval(t["call"], env) == X(t) for t in I[1]["widget"]["tests"] if "peak_heap" not in t["call"]))
# fix pass (finding 3): test 9 bounds the heap's peak size by the number of lists. Own k-way merge peaks at k = 20;
# one heap of every item peaks at N = 2,000. Measured here with a hand count, not the widget's prelude.
_ls = [list(range(i, 2000, 20)) for i in range(20)]
def _kway_peak(lists):
    import heapq as _h
    hp, peak = [(xs[0], i, 0) for i, xs in enumerate(lists) if xs], 0
    _h.heapify(hp); peak = len(hp)
    while hp:
        v, i, j = _h.heappop(hp)
        if j + 1 < len(lists[i]):
            _h.heappush(hp, (lists[i][j + 1], i, j + 1)); peak = max(peak, len(hp))
    return peak
_t9 = [t for t in I[1]["widget"]["tests"] if "peak_heap" in t["call"]]
check("hw i1 test 9: k-way merge peaks at k = 20, one heap of all items at N = 2,000, bound is 20",
      len(_t9) == 1 and _kway_peak(_ls) == 20 < sum(map(len, _ls)) == 2000 and _t9[0]["call"].endswith("<= 20")
      and I[1]["widget"]["tests"].index(_t9[0]) == 8 and I[1]["widget"]["tests"][9]["call"] == "NO_SORT")
env = {"running_median": lambda xs: [float(statistics.median(xs[:i + 1])) for i in range(len(xs))]}
small = [t for t in I[2]["widget"]["tests"] if "20000" not in t["call"]]
check("hw i2 expects against statistics.median", all(eval(t["call"], env) == X(t) for t in small))
data = [(i * 7919) % 10007 for i in range(20000)]
check("hw i2 tests 9 and 10", float(statistics.median(data)) == X(I[2]["widget"]["tests"][8]) and [float(statistics.median(data[:i + 1])) for i in range(0, 300, 37)] == X(I[2]["widget"]["tests"][9]))
try:
    hq = []; heapq.heappush(hq, (100.02, {"id": "A7"})); heapq.heappush(hq, (100.02, {"id": "A9"})); raised = False
except TypeError: raised = True
hq = []; heapq.heappush(hq, (100.02, {"id": "A7"})); heapq.heappush(hq, (100.03, {"id": "A9"}))
check("hw i4 dict tie raises TypeError; different prices do not", raised)
leaves = sum(1 for i in range(100) if 2 * i + 1 > 99)
check("hw i5 50 leaves in a heap of 100; slip 49", leaves == 50 == I[5]["widget"]["answer"])
bottom = 100 - (2 ** 6 - 1)
slip = {x["id"]: x["value"] for x in I[5]["widget"]["wrong"]}["levels"]
if slip != bottom:     # no feedback line names this slip, so no claim is false: a note, not a failing check
    print(f"NOTE  hw i5 slip 'levels' is {slip}; the bottom level of a 100-item heap holds {bottom} (audit note N1)")
def heapify_swaps(n):
    a = [Cnt(random.random()) for _ in range(n)]; Cnt.n = 0; heapq.heapify(a); return Cnt.n
check("hw i5 building a heap is linear: comparisons under 2n for n up to 200,000, ratio 2 when n doubles", heapify_swaps(200000) < 2.0 * 200000 and 1.9 < heapify_swaps(200000) / heapify_swaps(100000) < 2.1)
check("hw i6 tick band 90 to 110 has 2,001 slots", round((110 - 90) / 0.01) + 1 == 2001)
def save(n): return "#" if n is None else f"{n.val}," + save(n.left) + "," + save(n.right)
def loadt(text):
    tk = text.split(","); pos = [0]
    def rd():
        s = tk[pos[0]]; pos[0] += 1
        if s == "#": return None
        return N(int(s), rd(), rd())
    return rd()
env = {"build": build, "to_list": to_list, "save_tree": save, "load_tree": loadt, "balanced": balanced, "_line": save}
okh = True
for t in I[7]["widget"]["tests"]:
    loc = dict(env)
    if t.get("setup"): exec(t["setup"], loc)
    okh &= eval(t["call"], loc) == X(t)
check("hw i7 expects", okh and len(range(-2000, 2095)) == 4095)
okr = all((lambda t: to_list(loadt(save(t))) == to_list(t))(rand_tree(random.randint(0, 30))) for _ in range(500))
check("hw i7 pre-order with # round-trips (500 random trees, repeats and zeros included)", okr)

print(f"{PASS[0]} checks passed, {len(FAIL)} failed")

# =====================================================================================
# Part 3 (optional). --sweep <pkgs>: run every submission of Part 1 under the page's Pyodide.
# =====================================================================================
DRIVER = r'''
import fs from 'node:fs'; import path from 'node:path'; import { pathToFileURL } from 'node:url';
const [app, pkgs, subsFile] = process.argv.slice(2);
const { makeRunner } = await import(pathToFileURL(path.join(app, 'tools/code-runner.mjs')).href);
const runner = makeRunner({ pkgs, root: app, jobs: 4 });
const subs = JSON.parse(fs.readFileSync(subsFile, 'utf8'));
const cache = {};
const get = (file, p) => { const d = cache[file] ||= JSON.parse(fs.readFileSync(path.join(app, 'content/courses/ds', file), 'utf8')); return p.split('.').reduce((o, k) => { const m = /^(\w+)\[(\d+)\]$/.exec(k); return m ? o[m[1]][+m[2]] : o[k]; }, d); };
const out = [];
await Promise.all(subs.map(async (s, idx) => {
  const spec = get(s.file, s.path);
  let src = s.src;
  if (src === '@solution') src = spec.solution; else if (src === '@starter') src = spec.starter; else if (/^@mutant(\d+)$/.test(src)) src = spec.mutants[+src.slice(7)].source;
  const r = await runner.grade(spec, src, 'tests');
  const first = r.rows.findIndex((x) => !x.ok);
  const detail = first >= 0 ? String(r.rows[first].error || r.rows[first].actual).split('\n').slice(-1)[0].slice(0, 100) : '';
  out[idx] = { key: r.ok ? 'PASS' : r.key, detail };
}));
await runner.close();
let bad = 0;
subs.forEach((s, i) => { const o = out[i]; const diff = s.expect && s.expect !== o.key; if (diff) bad++; console.log(`${diff ? 'DIFF' : 'ok  '} | ${s.w} | ${s.name} | got ${o.key} | expected ${s.expect || '-'} | ${o.detail}`); });
process.exit(bad ? 1 : 0);
'''
if "--sweep" in sys.argv:
    pkgs = sys.argv[sys.argv.index("--sweep") + 1]
    d = tempfile.mkdtemp()
    json.dump(S_SUBS, open(os.path.join(d, "subs.json"), "w"))
    open(os.path.join(d, "driver.mjs"), "w").write(DRIVER)
    rc = subprocess.call(["node", os.path.join(d, "driver.mjs"), os.path.abspath(APP), pkgs, os.path.join(d, "subs.json")])
    if rc:
        FAIL.append("sweep")

sys.exit(1 if FAIL else 0)
