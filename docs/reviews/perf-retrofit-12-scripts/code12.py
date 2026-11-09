"""Reader runs for the six code items of batch 12 through harness12 (a mirror of code.js JUDGE).
For each item: the shipped solution (examples and tests), the starter, a reader solution written from the prose alone,
and the reader's own planted bugs, each with the tests it must fail. Run with the venv Python, or in Pyodide 0.27.7
through pyo12.mjs (packages: numpy sqlite3). Exit 0 when every expectation holds; a line marked GAP is a reader
finding (it is an expectation too: the GAP must reproduce)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from harness12 import item, summary, patched

fails = 0
PYO = sys.platform == "emscripten"


def expect(cond, msg):
    global fails
    if not cond:
        fails += 1
    print(("  ok   " if cond else "  FAIL ") + msg)


def check(w, label, src, must_fail=None, passes=False, which="tests"):
    f, r = summary(w, src, label, which)
    if passes:
        expect(not f, f"{label}: passes every {which}")
    elif must_fail is not None:
        expect(set(must_fail) <= set(f) and f, f"{label}: fails at least {must_fail}")
    return f, r


def shipped(w, name, starter_passes=()):
    check(w, name + " solution", w["solution"], passes=True, which="all")
    f, _ = summary(w, w["starter"], name + " starter")
    want = [i for i in range(1, len(w["tests"]) + 1) if i not in starter_passes]
    expect(f == want, f"{name} starter fails every hidden test" + (f" but {list(starter_passes)}" if starter_passes else ""))


# ---------------- sql L1 ----------------
it = item("sql", "homework-1.json", "h-cash-bonds")
w = it["widget"]
print("sql L1 h-cash-bonds")
shipped(w, "sql")
head = w["solution"].split("def query")[0]
q = lambda sql: head + "def query():\n    return " + repr(sql) + "\n"
import sqlite3
print("  sqlite", sqlite3.sqlite_version)
check(w, "reader: IN list, IS NOT NULL", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA', 'AA') AND maturity IS NOT NULL ORDER BY maturity ASC, yield DESC LIMIT 4"), passes=True)
check(w, "reader: NULLS LAST instead of a filter", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA', 'AA') ORDER BY maturity NULLS LAST, yield DESC LIMIT 4"), passes=True)
check(w, "reader: date() on maturity", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA','AA') AND date(maturity) IS NOT NULL ORDER BY date(maturity), yield DESC LIMIT 4"), passes=True)
check(w, "plant: rating >= 'AA' (lets BBB in)", q("SELECT bond, maturity, yield FROM bonds WHERE rating >= 'AA' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4"), [1])
check(w, "plant: rating LIKE 'A%' (lets A in)", q("SELECT bond, maturity, yield FROM bonds WHERE rating LIKE 'A%' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4"), [1])
check(w, "reader: rating NOT IN ('A', 'BBB') (NULL rating dropped by NOT IN)", q("SELECT bond, maturity, yield FROM bonds WHERE rating NOT IN ('A', 'BBB') AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4"), passes=True)
check(w, "plant: rating IS NOT 'A' AND rating IS NOT 'BBB' (NULL rating kept)", q("SELECT bond, maturity, yield FROM bonds WHERE rating IS NOT 'A' AND rating IS NOT 'BBB' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4"), [1])
check(w, "reader: maturity != '' (a NULL comparison is not true, so perpetuals drop)", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA','AA') AND maturity != '' ORDER BY maturity, yield DESC LIMIT 4"), passes=True)
check(w, "plant: no NULL test (perpetuals sort first)", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA','AA') ORDER BY maturity, yield DESC LIMIT 4"), [1])
check(w, "plant: tie broken by bond name (agrees with yield on the base table)", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA','AA') AND maturity IS NOT NULL ORDER BY maturity, bond LIMIT 4"), [3])
check(w, "plant: yield DESC applied first", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA','AA') AND maturity IS NOT NULL ORDER BY yield DESC, maturity LIMIT 4"), [1])
check(w, "plant: LIMIT 4 on maturity DESC (latest first)", q("SELECT bond, maturity, yield FROM bonds WHERE rating IN ('AAA','AA') AND maturity IS NOT NULL ORDER BY maturity DESC, yield DESC LIMIT 4"), [1])
check(w, "plant: SELECT * (four columns)", q("SELECT * FROM bonds WHERE rating IN ('AAA','AA') AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4"), [1, 2])

# ---------------- ds L4 ----------------
it = item("ds", "homework-4.json", "h4-save-tree")
w = it["widget"]
print("ds L4 h4-save-tree")
shipped(w, "ds")
reader = '''
def save_tree(root):
    if root is None:
        return "#"
    return f"{root.val},{save_tree(root.left)},{save_tree(root.right)}"

def load_tree(text):
    toks = text.split(",")
    def go(i):
        if toks[i] == "#":
            return None, i + 1
        node = Node(int(toks[i]))
        node.left, i = go(i + 1)
        node.right, i = go(i)
        return node, i
    return go(0)[0]
'''
check(w, "reader: string recursion, index passing", reader, passes=True, which="all")
check(w, "plant: empty tree saved as ''", patched(reader, ('return "#"\n', 'return ""\n')), [2])
check(w, "plant: values kept as str", patched(reader, ("Node(int(toks[i]))", "Node(toks[i])")), [3, 5])
check(w, "plant: in-order save", patched(reader, ('return f"{root.val},{save_tree(root.left)},{save_tree(root.right)}"', 'return f"{save_tree(root.left)},{root.val},{save_tree(root.right)}"')), [1])
check(w, "plant: no mark under a leaf", patched(reader, ('    if root is None:\n        return "#"\n', '    if root is None:\n        return "#"\n    if root.left is None and root.right is None:\n        return str(root.val)\n')), [1])
check(w, "plant: split with ', '", patched(reader, ('text.split(",")', 'text.split(", ")')), [5])
check(w, "plant: right side read first", patched(reader, ("        node.left, i = go(i + 1)\n        node.right, i = go(i)", "        node.right, i = go(i + 1)\n        node.left, i = go(i)")), [5])

# ---------------- vectors L3 ----------------
it = item("vectors", "homework-3.json", "h-bond-curve")
w = it["widget"]
print("vectors L3 h-bond-curve" + (" (Pyodide)" if PYO else " (CPython)"))
shipped(w, "vectors", starter_passes=(12,))   # test 12 only reads the source for inv(
import numpy as np
print("  numpy", np.__version__)
A = np.array([[102.0, 0, 0], [105, 0, 0], [4, 4, 104]])
B = np.array([[2.1, 2.1, 102.1], [3.3, 3.3, 103.3], [4.7, 4.7, 104.7]])
for name, M in (("test 8", A), ("test 9", B)):
    try:
        x = np.linalg.solve(M, np.ones(3))
        how = "returns " + np.array2string(x, precision=3)
    except np.linalg.LinAlgError as e:
        how = "raises LinAlgError"
    print(f"  {name}: det {np.linalg.det(M):.3e}, rank {np.linalg.matrix_rank(M)}, solve {how}")
reader = '''
import numpy as np

def rows(bonds, n):
    out = []
    for c, m in bonds:
        if not 1 <= m <= n:
            raise ValueError("maturity off the curve")
        out.append([c] * (m - 1) + [c + 100] + [0] * (n - m))
    return np.array(out, dtype=float)

def curve_from_bonds(bonds, prices, targets):
    n = max(m for c, m in bonds)
    C = rows(bonds, n)
    if C.shape != (n, n):
        raise ValueError("need one bond per year")
    s = np.linalg.svd(C, compute_uv=False)
    if s[-1] <= 1e-10 * s[0]:
        raise ValueError("the bonds do not fix the curve")
    d = np.linalg.solve(C, np.asarray(prices, dtype=float))
    return d, rows(targets, n) @ d
'''
check(w, "reader: lists of rows, SVD condition", reader, passes=True, which="all")
lst = patched(reader, ("    d = np.linalg.solve(C, np.asarray(prices, dtype=float))", "    d = np.linalg.lstsq(C, np.asarray(prices, dtype=float), rcond=None)[0]"))
check(w, "reader: lstsq after the rank check", lst, passes=True)
nocheck = patched(reader, ('''    s = np.linalg.svd(C, compute_uv=False)
    if s[-1] <= 1e-10 * s[0]:
        raise ValueError("the bonds do not fix the curve")
''', ""))
f_no, _ = check(w, "plant: no singularity check", nocheck, [9])
expect((8 in f_no) == PYO, f"plant no-check: test 8 {'fails (NaN, no error)' if PYO else 'passes by accident (LinAlgError is a ValueError)'}")
det = patched(reader, ('''    s = np.linalg.svd(C, compute_uv=False)
    if s[-1] <= 1e-10 * s[0]:''', '''    if np.linalg.det(C) == 0:'''))
f_det, _ = check(w, "plant: det == 0", det, [9])
nan = patched(nocheck, ("    return d, rows(targets, n) @ d", "    if np.isnan(d).any():\n        raise ValueError('singular')\n    return d, rows(targets, n) @ d"))
f_nan, _ = check(w, "plant: NaN check after solve (the prose's hint)", nan, [9])
expect(8 not in f_nan, "plant NaN check: test 8 passes in both runtimes (NaN in Pyodide, LinAlgError in CPython)")
check(w, "plant: no target maturity check (IndexError)", patched(reader, ("        if not 1 <= m <= n:\n            raise ValueError(\"maturity off the curve\")\n", ""), ("+ [0] * (n - m))", "+ [0] * (n - m))\n        if len(out[-1]) != n:\n            raise IndexError('long row')")), [10])
check(w, "plant: inverse", patched(reader, ("np.linalg.solve(C, np.asarray(prices, dtype=float))", "np.linalg.inv(C) @ np.asarray(prices, dtype=float)")), [12])
check(w, "plant: bootstrap that needs a one-year bond", '''
import numpy as np
def curve_from_bonds(bonds, prices, targets):
    n = max(m for c, m in bonds)
    if len(bonds) != n:
        raise ValueError("count")
    order = sorted(range(n), key=lambda i: bonds[i][1])
    if [bonds[i][1] for i in order] != list(range(1, n + 1)):
        raise ValueError("one bond per maturity")
    d = []
    for i in order:
        c, m = bonds[i]
        d.append((prices[i] - c * sum(d)) / (c + 100))
    for c, m in targets:
        if m > n:
            raise ValueError("long target")
    d = np.array(d)
    return d, np.array([c * d[:m].sum() + 100 * d[m - 1] for c, m in targets])
''', [3, 4])
check(w, "plant: coupon left out at maturity", patched(reader, ("[c + 100]", "[100]")), [1])

# ---------------- random-vars L1 ----------------
it = item("random-vars", "homework-1.json", "h-build-pmf")
w = it["widget"]
print("random-vars L1 h-build-pmf")
shipped(w, "random-vars")
reader = '''
import math
from collections import defaultdict

def pmf_of(space, X):
    ps = list(space.values())
    if min(ps, default=0) < 0 or not math.isclose(math.fsum(ps), 1, rel_tol=0, abs_tol=1e-9):
        raise ValueError("not a probability space")
    out = defaultdict(int)
    for w, p in space.items():
        out[X(w)] += p
    return {x: p for x, p in out.items() if p != 0}
'''
check(w, "reader: fsum, defaultdict, zeros dropped at the end", reader, passes=True, which="all")
check(w, "plant: total compared with == 1 (running sum)", patched(reader, ("not math.isclose(math.fsum(ps), 1, rel_tol=0, abs_tol=1e-9)", "sum(ps) != 1")), [7])
check(w, "plant: no negative check", patched(reader, ("min(ps, default=0) < 0 or ", "")), [10])
check(w, "plant: zero-chance values kept", patched(reader, (" if p != 0}", "}")), [5])
check(w, "plant: counts outcomes, not chances", patched(reader, ("out[X(w)] += p", "out[X(w)] += 1 / len(space)")), [3])
check(w, "plant: tolerance 1e-3", patched(reader, ("abs_tol=1e-9", "abs_tol=1e-3")), [9])
check(w, "plant: returns the outcome lists", patched(reader, ("return {x: p for x, p in out.items() if p != 0}", "return {x: [v for v in space if X(v) == x] for x, p in out.items() if p != 0}")), [1])

# ---------------- algo-think L2 ----------------
it = item("algo-think", "homework-2.json", "h-split-feed")
w = it["widget"]
print("algo-think L2 h-split-feed")
shipped(w, "algo-think L2")
reader = '''
from functools import lru_cache

def split_feed(feed, listed):
    names = tuple(sorted(set(listed)))
    @lru_cache(maxsize=None)
    def go(i):
        if i == len(feed):
            return ((),)
        out = []
        for j in range(i + 1, len(feed) + 1):
            if feed[i:j] in names:
                out += [(feed[i:j],) + rest for rest in go(j)]
        return tuple(out)
    return [list(s) for s in go(0)]
'''
check(w, "reader: memoised cut positions", reader, passes=True, which="all")
check(w, "plant: base case [] (no split)", patched(reader, ("return ((),)", "return ()")), [1, 2])
check(w, "plant: cuts stop one short of the end", patched(reader, ("range(i + 1, len(feed) + 1)", "range(i + 1, len(feed))")), [1, 7])
check(w, "plant: first matching cut only", patched(reader, ("                out += [(feed[i:j],) + rest for rest in go(j)]", "                out += [(feed[i:j],) + rest for rest in go(j)]\n                if out:\n                    break")), [5])
check(w, "plant: listed walked as given (duplicates)", '''
def split_feed(feed, listed):
    if feed == "":
        return [[]]
    out = []
    for t in listed:
        if feed.startswith(t):
            out += [[t] + r for r in split_feed(feed[len(t):], listed)]
    return out
''', [5])
check(w, "plant: listed sorted in place to dedupe", '''
def split_feed(feed, listed):
    listed.sort()
    names = [t for i, t in enumerate(listed) if i == 0 or listed[i - 1] != t]
    if feed == "":
        return [[]]
    out = []
    for t in names:
        if feed.startswith(t):
            out += [[t] + r for r in split_feed(feed[len(t):], names)]
    return out
''', [12])

# ---------------- algo-think L3 ----------------
it = item("algo-think", "homework-3.json", "h-ring-search")
w = it["widget"]
print("algo-think L3 h-ring-search")
shipped(w, "algo-think L3")
reader = '''
def find_trade(ring, seq):
    n = len(ring)
    if n == 0:
        return -1
    lo, hi = 0, n - 1                 # find the oldest slot: the first slot below ring[-1] or slot 0
    while lo < hi:
        mid = (lo + hi) // 2
        if ring[mid] > ring[hi]:
            lo = mid + 1
        else:
            hi = mid
    k = lo
    lo, hi = 0, n - 1                 # plain binary search on the sorted order, slot = (i + k) % n
    while lo <= hi:
        mid = (lo + hi) // 2
        v = ring[(mid + k) % n]
        if v == seq:
            return (mid + k) % n
        if v < seq:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
'''
check(w, "reader: find the turn, then search in sorted order", reader, passes=True, which="all")
check(w, "reader variant: turn found with >= (same as > on distinct numbers)", patched(reader, ("if ring[mid] > ring[hi]:", "if ring[mid] >= ring[hi]:")), passes=True)
check(w, "GAP: turn found by ring.index(min(ring)), O(n)", '''
def find_trade(ring, seq):
    if not ring:
        return -1
    k = ring.index(min(ring))
    n = len(ring)
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = ring[(mid + k) % n]
        if v == seq:
            return (mid + k) % n
        if v < seq:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
''', passes=True)
check(w, "plant: second search stops at lo < hi", patched(reader, ("    while lo <= hi:\n        mid = (lo + hi) // 2\n        v", "    while lo < hi:\n        mid = (lo + hi) // 2\n        v")), [7])
check(w, "plant: slot not shifted back by the turn", patched(reader, ("            return (mid + k) % n", "            return mid")), [1])
check(w, "plant: unturned shortcut read before the empty guard", patched(reader, ("    if n == 0:\n        return -1\n", "    if ring[0] <= ring[-1]:\n        k = 0\n    if n == 0:\n        return -1\n")), [2])
lin = "def find_trade(ring, seq):\n    return ring.index(seq) if seq in ring else -1\n"
check(w, "GAP: a linear scan (no binary search)", lin, passes=True)

print(f"failures: {fails}")
sys.exit(1 if fails else 0)
