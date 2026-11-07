"""Recompute every figure of coding-int homework-3 item h3-notes-drive (performance task, L3).

Route 1: the item's own solution. Route 2: an independent flat reference (a dict of file
paths and a set of folder paths, size by scanning). Every test expectation must agree on both.
Also: the starter fails every test, planted wrong solutions each fail the test named for them,
the walk-the-subtree size is far slower than the solution on test 10, and the counts in the
prose and `how` match the file. Run: python3 -I docs/reports/coding-int-3-perf-numbers.py
"""
import json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'coding-int', 'homework-3.json')
doc = json.load(open(HW))
items = doc['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h3-notes-drive']
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


class Ref:
    """Flat reference: no tree at all."""
    def __init__(self):
        self.files, self.dirs = {}, {()}

    @staticmethod
    def p(path):
        return tuple(x for x in path.split('/') if x)

    def _dirs_above(self, t):
        for k in range(len(t)):
            self.dirs.add(t[:k])

    def exists(self, t):
        return t in self.files or t in self.dirs

    def mkdir(self, path):
        t = self.p(path)
        self._dirs_above(t)
        self.dirs.add(t)

    def write(self, path, text):
        t = self.p(path)
        self._dirs_above(t)
        self.files[t] = text

    def read(self, path):
        return self.files.get(self.p(path))

    def ls(self, path):
        t = self.p(path)
        if t in self.files:
            return [t[-1]]
        if t not in self.dirs:
            return []
        kids = {x[len(t)] for x in list(self.files) + list(self.dirs) if len(x) > len(t) and x[:len(t)] == t}
        return sorted(kids)

    def _under(self, t):
        return [x for x in list(self.files) + list(self.dirs) if x[:len(t)] == t]

    def rm(self, path):
        t = self.p(path)
        if not t or not self.exists(t):
            return
        for x in self._under(t):
            self.files.pop(x, None)
            self.dirs.discard(x)

    def mv(self, src, dst):
        s, d = self.p(src), self.p(dst)
        if not s or not self.exists(s) or self.exists(d) or d[:len(s)] == s:
            return False
        moved_f = {x: v for x, v in self.files.items() if x[:len(s)] == s}
        moved_d = {x for x in self.dirs if x[:len(s)] == s}
        for x in moved_f:
            del self.files[x]
        self.dirs -= moved_d
        self._dirs_above(d)
        for x, v in moved_f.items():
            self.files[d + x[len(s):]] = v
        for x in moved_d:
            self.dirs.add(d + x[len(s):])
        return True

    def size(self, path):
        t = self.p(path)
        return sum(len(v) for x, v in self.files.items() if x[:len(t)] == t)


def namespace(code, cls=None):
    ns = {}
    exec(code, ns)
    if cls is not None:
        ns['FileSystem'] = cls
    exec(w['postlude'], ns)
    return ns


def run_tests(ns, limit_index=None):
    """Return the list of 1-based test numbers that fail (an exception is a failure)."""
    bad = []
    for k, t in enumerate(w['tests'], 1):
        if limit_index is not None and k > limit_index:
            break
        try:
            got = eval(t['call'], ns)
            ok = got == eval(t['expect'])
        except Exception:
            ok = False
        if not ok:
            bad.append(k)
    return bad


# 1. Every expectation, two routes.
sol_ns = namespace(w['solution'])
ref_ns = namespace('', Ref)
for k, t in enumerate(w['tests'], 1):
    want = eval(t['expect'])
    a = eval(t['call'], sol_ns)
    b = eval(t['call'], ref_ns)
    check(a == want and b == want, f'test {k}: solution {a!r}, reference {b!r}, file {want!r}')

# 2. Examples are tests 1 and 2; counts.
check(w['examples'] == w['tests'][:2], 'examples equal tests 1 and 2')
check(len(w['tests']) == 10 and len(w['examples']) == 2, '10 tests, 2 examples')
check('10 hidden tests' in w['how'] and '100,000 random steps' in w['how'], 'how names 10 tests and 100,000 steps')
check('def big_case(n=100000)' in w['postlude'], 'big_case default n is 100,000')
check(len(items) == 9, 'homework-3 now holds 9 items (cap 12)')
check(sum(1 for it in items if it.get('performance')) == 1, 'one performance item in the level homework')

# 3. Starter fails every test.
st_bad = run_tests(namespace(w['starter']))
check(st_bad == list(range(1, 11)), f'starter fails tests {st_bad}')

# 4. Planted wrong solutions, each by an exact text change to the solution.
S = w['solution']
mutants = {
    'append instead of replace': (
        "        self._add(chain[:-1], len(text) - node.total)\n        node.text, node.total = text, len(text)",
        "        self._add(chain[:-1], len(text))\n        node.text = (node.text or '') + text\n        node.total = len(node.text)", 3),
    'adds the new length, not the change': (
        "self._add(chain[:-1], len(text) - node.total)", "self._add(chain[:-1], len(text))", 3),
    'refusals after making dst folders': (
        "        s, d = self._names(src), self._names(dst)\n",
        "        s, d = self._names(src), self._names(dst)\n        self._make(d[:-1])\n", 6),
    'string prefix for inside': (
        "or d[:len(s)] == s:", "or dst.startswith(src):", 7),
    'mv leaves the totals': (
        "        self._add(target, node.total)\n", "", 2),
    'mv takes totals off src only': (
        "        self._add(target, node.total)\n", "        self._add(target[:1], node.total)\n", 2),
    'rm leaves the totals': (
        "        self._add(chain[:-1], -chain[-1].total)\n        del chain[-2]", "        del chain[-2]", 4),
    'rm of / clears everything': (
        "        if not names or chain is None:\n            return\n",
        "        if not names:\n            self.root = _Node()\n            return\n        if chain is None:\n            return\n", 4),
    'mv overwrites an existing dst': (
        " or self._chain(d) is not None", "", 6),
    'ls of a file gives []': (
        "            return [names[-1]]", "            return []", 1),
}
for name, (old, new, first) in mutants.items():
    check(S.count(old) == 1, f'mutant "{name}": text found once')
    bad = run_tests(namespace(S.replace(old, new)), limit_index=9)
    check(bool(bad) and bad[0] == first, f'mutant "{name}" first fails test {bad[:1]} (named {first}), fails {bad}')

# byKey names: every keyed test is the first failure of some mutant, except the timing test.
firsts = {m[2] for m in mutants.values()}
for key in item['feedback']['byKey']:
    n = int(key.split('-')[1])
    check(n in firsts or n == 10, f'byKey {key} is a planted slip or the timing test')

# 5. Timing: walk-the-subtree size against the solution on test 10.
slow = S.replace(
    "    def size(self, path):\n        chain = self._chain(self._names(path))\n        return 0 if chain is None else chain[-1].total\n",
    "    def size(self, path):\n        chain = self._chain(self._names(path))\n        if chain is None:\n            return 0\n"
    "        def total(n):\n            if n.text is not None:\n                return len(n.text)\n"
    "            return sum(total(c) for c in n.children.values())\n        return total(chain[-1])\n")
check(slow != S, 'slow size built')
times = {}
for label, code in (('solution', S), ('walk size', slow)):
    ns = namespace(code)
    t0 = time.perf_counter()
    got = eval('big_case()', ns)
    times[label] = time.perf_counter() - t0
    check(got == eval(w['tests'][9]['expect']), f'{label} gets test 10 right in {times[label]:.2f} s')
check(times['solution'] < 1.0 and times['walk size'] > 5.0, 'solution under 1 s, walk size over 5 s (CPython)')

# 6. Hand counts of the example figures.
check(len('hello') + len('abc') == 8 and len('abc') == 3, 'example 1 sizes 8 and 3')
check(4 + 6 + 1 + 2 - 6 + 1 == 8 and 2 + 4 + 6 == 12, 'test 8 sizes 12 then 8')

print('failures:', fails)
sys.exit(1 if fails else 0)
