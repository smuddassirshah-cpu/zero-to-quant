"""Recompute every figure of ds homework-4 item h4-save-tree (performance task, L4).

Route 1: the item's own solution (recursive pre-order save, one shared iterator on load).
Route 2: an independent pair written here (save by returning strings, load with an explicit
stack), run against the same tests; and every literal `expect` recomputed from it.
Also: the starter fails; each planted wrong solution fails first at the test named below;
two slow but correct solutions (pop(0) load, string-concatenation save) pass inside 5 s;
the counts in `how` and byKey match the file. Run: python3 -I docs/reports/ds-4-perf-numbers.py
"""
import json, os, signal, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'ds', 'homework-4.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h4-save-tree']
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
E = w['examples']
print('item index (1-based):', idx[0] + 1, 'of', len(items))
check(item.get('performance') == 'code', 'performance kind is code')
check(len(T) >= 3 and len(T) > len(E), f'{len(T)} tests > {len(E)} examples')
check(all(any(e['call'] == t['call'] and e['expect'] == t['expect'] for t in T) for e in E),
      'every example is also a hidden test')


class Slow(Exception):
    pass


def _alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, _alarm)


def same(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y)
                and all(same(p, q) for p, q in zip(x, y)))
    return type(x) == type(y) and x == y if not (isinstance(x, bool) or isinstance(y, bool)) else x is y


def namespace(code):
    ns = {'__name__': '__main__', '__learner_source__': code}
    exec(w['prelude'], ns)
    exec(code, ns)
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
            if 'setup' in t:
                exec(t['setup'], ns)
            ok = same(eval(t['call'], ns), eval(t['expect'], ns))
        except (Exception, Slow, RecursionError):
            ok = False
        signal.setitimer(signal.ITIMER_REAL, 0)
        secs.append(time.perf_counter() - t0)
        if not ok:
            bad.append(k)
    return bad, secs


# ---- route 1 and route 2 pass every test; the starter fails ----
bad, secs = run_tests(w['solution'])
check(bad == [], f'solution passes all {len(T)} tests (max {max(secs):.3f} s)')

ROUTE2 = '''
def save_tree(root):
    if root is None:
        return "#"
    return str(root.val) + "," + save_tree(root.left) + "," + save_tree(root.right)

def load_tree(text):
    toks = text.split(",")
    if toks[0] == "#":
        return None
    root = Node(int(toks[0]))
    stack = [[root, 0]]          # node, children filled so far
    for tok in toks[1:]:
        parent = stack[-1]
        child = None if tok == "#" else Node(int(tok))
        if parent[1] == 0:
            parent[0].left = child
        else:
            parent[0].right = child
        parent[1] += 1
        while stack and stack[-1][1] == 2:
            stack.pop()
        if child is not None:
            stack.append([child, 0])
    return root
'''
bad, secs = run_tests(ROUTE2)
check(bad == [], f'route 2 (string save, stack load) passes all tests (max {max(secs):.3f} s)')

bad, _ = run_tests(w['starter'])
check(len(bad) >= len(T) - 1, f'starter fails {len(bad)} of {len(T)} tests')

# ---- every literal expect recomputed by route 2 ----
ns2 = namespace(ROUTE2)
for k, t in enumerate(T, 1):
    if 'setup' in t:
        continue
    got = eval(t['call'], ns2)
    want = eval(t['expect'], ns2)
    check(same(got, want), f'test {k} expect {t["expect"]} recomputed: {got!r}')

# hand check of the two worked strings in the question and test 4
check(ns2['save_tree'](ns2['build']([1, 2, 3])) == '1,2,#,#,3,#,#', 'question example string')
check(ns2['save_tree'](None) == '#', 'empty tree is #')
check(ns2['_line'](ns2['build']([5, 3, 6, 2, 4, None, None, 1])) == '5,3,2,1,#,#,#,4,#,#,6,#,#',
      'prelude _line agrees with route 2 on test 4')

# ---- the 4,095 nodes in how ----
ns2['big'] = ns2['balanced'](list(range(-2000, 2095)))
n_nodes = sum(v is not None for v in ns2['to_list'](ns2['big']))
line = ns2['save_tree'](ns2['big'])
check(n_nodes == 4095 == len(range(-2000, 2095)), f'big tree has {n_nodes} nodes')
check(line.count('#') == n_nodes + 1 and len(line.split(',')) == 2 * n_nodes + 1,
      f'big line has {len(line.split(","))} tokens, {line.count("#")} marks')
check(line == ns2['_line'](ns2['big']), 'route 2 save equals prelude _line on big')
check('Check runs 11 hidden tests' in w['how'] and len(T) == 11, 'how: 11 hidden tests')
check('4,095 nodes' in w['how'] and all('setup' in T[k - 1] for k in (10, 11)), 'how: tests 10 and 11, 4,095 nodes')

# ---- planted wrong solutions: (name, code, first failing test) ----
SOL = w['solution']
PLANTED = [
    ('empty tree saves as empty string',
     SOL.replace('    out = []\n', '    if root is None:\n        return ""\n    out = []\n'), 2),
    ('splits the line into characters',
     SOL.replace('iter(text.split(","))', 'iter([c for c in text if c != ","])'), 5),
    ('keeps values as strings', SOL.replace('Node(int(tok))', 'Node(tok)'), 3),
    ('reading position global, not reset per call', SOL.replace(
        'def load_tree(text):\n    tokens = iter(text.split(","))\n',
        '_POS = [0]\n\ndef load_tree(text):\n    toks = text.split(",")\n'
        '    def nxt():\n        _POS[0] += 1\n        return toks[_POS[0] - 1]\n'
        '    tokens = None\n').replace('tok = next(tokens)', 'tok = nxt()'), 3),
    ('in-order save', SOL.replace(
        '        out.append(str(node.val))\n        walk(node.left)\n',
        '        walk(node.left)\n        out.append(str(node.val))\n'), 1),
    ('level-order save with marks', SOL.replace('''    out = []

    def walk(node):
        if node is None:
            out.append("#")
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)''', '''    out, q = [], [root]
    while q:
        node = q.pop(0)
        if node is None:
            out.append("#")
            continue
        out.append(str(node.val))
        q.append(node.left)
        q.append(node.right)
    return ",".join(out)'''), 1),
    ('0 read as empty', SOL.replace(
        '        node = Node(int(tok))\n',
        '        if not int(tok):\n            return None\n        node = Node(int(tok))\n'), 5),
    ('load fills the right side first', SOL.replace(
        '        node.left = read()\n        node.right = read()\n',
        '        node.right = read()\n        node.left = read()\n'), 5),
    ('no marks below a leaf', SOL.replace(
        '        out.append(str(node.val))\n',
        '        out.append(str(node.val))\n        if node.left is None and node.right is None:\n            return\n'), 1),
    ('comma and space between values', SOL.replace('return ",".join(out)', 'return ", ".join(out)'), 1),
    ('load ignores marks and inserts as a BST', SOL.replace('''    tokens = iter(text.split(","))

    def read():
        tok = next(tokens)
        if tok == "#":
            return None
        node = Node(int(tok))
        node.left = read()
        node.right = read()
        return node

    return read()''', '''    root = None
    for tok in text.split(","):
        if tok == "#":
            continue
        v, node, parent = int(tok), root, None
        while node:
            parent, node = node, (node.left if v < node.val else node.right)
        if parent is None:
            root = Node(v)
        elif v < parent.val:
            parent.left = Node(v)
        else:
            parent.right = Node(v)
    return root'''), 5),
    ('pre-order with no marks at all', SOL.replace('            out.append("#")\n', '            pass\n'), 1),
]
for name, code, first in PLANTED:
    check(code != SOL, f'planted "{name}" differs from the solution')
    bad, _ = run_tests(code)
    check(bad and bad[0] == first, f'planted "{name}" first fails test {first} (fails {bad})')
firsts = {first for _, _, first in PLANTED}
check(len(PLANTED) >= 3 and len(firsts) >= 3, f'{len(PLANTED)} planted slips, first fails at tests {sorted(firsts)}')
for key in item['feedback']['byKey']:
    check(int(key.split('-')[1]) in firsts, f'byKey {key} names a test a planted slip first fails')

# ---- slow but correct solutions still pass inside 5 s ----
SLOW = '''
def save_tree(root):
    s = ""
    def walk(node):
        nonlocal s
        if node is None:
            s = s + "#,"
            return
        s = s + str(node.val) + ","
        walk(node.left)
        walk(node.right)
    walk(root)
    return s[:-1]

def load_tree(text):
    toks = text.split(",")
    def read():
        tok = toks.pop(0)
        if tok == "#":
            return None
        node = Node(int(tok))
        node.left = read()
        node.right = read()
        return node
    return read()
'''
bad, secs = run_tests(SLOW)
check(bad == [], f'slow but correct (pop(0), string +) passes; tests 10, 11 take {secs[9]:.3f} s, {secs[10]:.3f} s')

print('FAILURES:', fails)
sys.exit(1 if fails else 0)
