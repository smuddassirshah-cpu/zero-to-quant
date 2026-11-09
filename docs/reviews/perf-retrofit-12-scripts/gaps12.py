"""Gap checks and proposed fixes for batch 12 (findings AT3-1, RV1-1). Run with the venv Python, or in Pyodide via pyo12.mjs.
AT3-1: a linear scan passes every test of algo-think h-ring-search. The test (now in the item) counts reads with the Looks
wrapper that algo-think l9 already uses; this script measures the reads of the shipped solution, two reader binary
searches and three O(n) answers, then runs the item and checks who passes.
RV1-1: in Python 3.12 (Pyodide 0.27.7) the built-in sum of ten 0.1s is exactly 1.0, so the explain's example
holds only for a running total."""
import sys, json, copy, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from harness12 import item, summary

fails = 0


def expect(c, m):
    global fails
    fails += 0 if c else 1
    print(("ok   " if c else "FAIL ") + m)


LOOKS = '''
class Looks:
    def __init__(self, data):
        self.data = list(data)
        self.looks = 0
    def __len__(self):
        return len(self.data)
    def __getitem__(self, i):
        self.looks += 1
        return self.data[i]
'''
w0 = item("algo-think", "homework-3.json", "h-ring-search")["widget"]
two_phase = '''
def find_trade(ring, seq):
    n = len(ring)
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if ring[mid] > ring[hi]:
            lo = mid + 1
        else:
            hi = mid
    k = lo
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
'''
recursive = '''
def find_trade(ring, seq, lo=0, hi=None):
    if hi is None:
        hi = len(ring) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    m, a, b = ring[mid], ring[lo], ring[hi]
    if m == seq:
        return mid
    if a <= m:
        if a <= seq < m:
            return find_trade(ring, seq, lo, mid - 1)
        return find_trade(ring, seq, mid + 1, hi)
    if m < seq <= b:
        return find_trade(ring, seq, mid + 1, hi)
    return find_trade(ring, seq, lo, mid - 1)
'''
linear = "def find_trade(ring, seq):\n    return ring.index(seq) if seq in ring else -1\n"
loop = "def find_trade(ring, seq):\n    for i in range(len(ring)):\n        if ring[i] == seq:\n            return i\n    return -1\n"
minidx = '''
def find_trade(ring, seq):
    if len(ring) == 0:
        return -1
    vals = [ring[i] for i in range(len(ring))]
    k = vals.index(min(vals))
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
'''
SRC = {"shipped": w0["solution"], "two-phase": two_phase, "recursive": recursive}
R = [1000000 + 3 * ((j + 137017) % 200000) for j in range(200000)]
probe = [R[0], R[-1], 1000000, 1599997, 1300000, 1300001, 999997, 1600000] + R[::997]
for name, src in SRC.items():
    g = {}
    exec(LOOKS + src, g)
    worst = 0
    for s in probe:
        L = g["Looks"](R)
        got = g["find_trade"](L, s)
        want = R.index(s) if s in R else -1
        expect(got == want, f"{name}: right slot for {s}") if got != want else None
        worst = max(worst, L.looks)
    print(f"  {name}: most reads over {len(probe)} searches of 200,000 slots: {worst}")
    expect(worst <= 120, f"{name}: at most 120 reads")

# The fix is now in the item: widget.prelude holds Looks and test 13 counts the reads (the fix pass of review-perf-retrofit-12).
w = w0
assert w["prelude"].lstrip().startswith("class Looks") and "W.looks <= 400" in w["tests"][12]["call"]
for name, src, ok_ in [("shipped", w0["solution"], True), ("two-phase", two_phase, True), ("recursive", recursive, True),
                       ("linear (index)", linear, False), ("linear (loop)", loop, False), ("turn by min() then halving", minidx, False)]:
    f, _ = summary(w, src, "fixed item: " + name)
    expect((not f) if ok_ else (f == [13]), f"fixed item: {name} {'passes' if ok_ else 'fails test 13 only'}")

# RV1-1
vals = [0.1] * 10
run = 0.0
for v in vals:
    run += v
print(f"Python {sys.version.split()[0]}: sum(ten 0.1) = {sum(vals)!r}, running total = {run!r}")
expect(run != 1.0, "a running total of ten 0.1s is not 1.0")
if sys.version_info >= (3, 12):
    expect(sum(vals) == 1.0, "Python 3.12+: the built-in sum of ten 0.1s is exactly 1.0 (RV1-1)")

print(f"failures: {fails}")
sys.exit(1 if fails else 0)
