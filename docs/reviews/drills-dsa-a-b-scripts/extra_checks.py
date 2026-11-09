# Extra planted solutions and proposed new tests for findings in review-drills-dsa-a-b.md.
# Run: <venv python> extra_checks.py <drills dir>
# Part 1 shows wrong or off-target solutions that pass every hidden test of a drill.
# Part 2 computes the expect of each proposed new test with the reader's own solutions,
# and shows the planted solution failing it.
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mine_a, mine_b

DDIR = sys.argv[1]


def run_all(fn_name, impl, did):
    d = json.load(open(os.path.join(DDIR, did + '.json')))
    ns = {fn_name: impl}
    bad = 0
    t0 = time.time()
    for c in d['examples'] + d['tests']:
        if eval(c['call'], dict(ns)) != eval(c['expect']):
            bad += 1
    return bad, len(d['examples']) + len(d['tests']), time.time() - t0


# ---- planted solutions that pass everything ----

def varied_first_last(badges, k):
    """Wrong: a window counts when its first and last badge differ."""
    n = len(badges)
    if k > n:
        return 0
    if k == 1:
        return n
    return sum(1 for i in range(n - k + 1) if badges[i] != badges[i + k - 1])


def sensor_float(text):
    """Uses true division, which the note says rounds away a near miss."""
    tok = text.split()
    n, k, t = int(tok[0]), int(tok[1]), int(tok[2])
    r = [int(x) for x in tok[3:3 + n]]
    if k > n:
        return '0'
    s = sum(r[:k])
    c = int(s / k >= t)
    for i in range(k, n):
        s += r[i] - r[i - k]
        c += s / k >= t
    return str(c)


def sensor_floor(text):
    """Uses floor division of the window sum."""
    tok = text.split()
    n, k, t = int(tok[0]), int(tok[1]), int(tok[2])
    r = [int(x) for x in tok[3:3 + n]]
    if k > n:
        return '0'
    s = sum(r[:k])
    c = int(s // k >= t)
    for i in range(k, n):
        s += r[i] - r[i - k]
        c += s // k >= t
    return str(c)


def kiosk_walk_down(sites, k):
    """The brief's 'slow' method: try every gap in turn, from the even split down."""
    s = sorted(sites)

    def ok(g):
        c, last = 1, s[0]
        for x in s[1:]:
            if x - last >= g:
                c += 1
                last = x
        return c >= k

    g = (s[-1] - s[0]) // (k - 1)
    while not ok(g):
        g -= 1
    return g


def net_fifo(orders):
    """Wrong: sells net against the oldest buy first."""
    from collections import deque
    q, neg = deque(), []
    for o in orders:
        if o > 0:
            q.append(o)
        else:
            s = -o
            while s and q:
                if q[0] > s:
                    q[0] -= s
                    s = 0
                else:
                    s -= q.popleft()
            if s:
                neg.append(-s)
    return neg + list(q)


def net_merge(orders):
    """Wrong by the brief: resting sells merge into one entry."""
    st = []
    for o in orders:
        if o > 0:
            st.append(o)
        else:
            s = -o
            while s and st and st[-1] > 0:
                if st[-1] > s:
                    st[-1] -= s
                    s = 0
                else:
                    s -= st.pop()
            if s:
                if st and st[-1] < 0:
                    st[-1] -= s
                else:
                    st.append(-s)
    return st


def hedge_dedupe(sizes, target):
    """Wrong: works on distinct sizes, with a patch for an all-equal list."""
    s = sorted(set(sizes))
    if len(s) == 1:
        return abs(2 * s[0] - target)
    i, j, best = 0, len(s) - 1, None
    while i < j:
        v = s[i] + s[j] - target
        best = abs(v) if best is None else min(best, abs(v))
        if v < 0:
            i += 1
        else:
            j -= 1
    return best


def flattest_min_or_total(pnl):
    """Wrong: best single day or the full total. Passes the first large test only."""
    return min(min(abs(x) for x in pnl), abs(sum(pnl)))


print('Part 1: planted solutions run on every example and hidden test (failures / cases, seconds)')
for name, fn, impl, did in [
    ('varied: first != last', 'count_varied_windows', varied_first_last, 'dsa-varied-windows'),
    ('sensor: true division', 'solve_sensor_alarm', sensor_float, 'dsa-sensor-alarm'),
    ('sensor: floor division', 'solve_sensor_alarm', sensor_floor, 'dsa-sensor-alarm'),
    ('kiosk: walk down from even split', 'widest_spacing', kiosk_walk_down, 'dsa-kiosk-spacing'),
    ('net: FIFO', 'net_tape', net_fifo, 'dsa-net-tape'),
    ('net: merged sells', 'net_tape', net_merge, 'dsa-net-tape'),
    ('hedge: distinct sizes', 'closest_pair_gap', hedge_dedupe, 'dsa-closest-hedge'),
]:
    bad, tot, dt = run_all(fn, impl, did)
    print(f'  {name:36s} {bad}/{tot} fail, {dt:.2f}s')

print('Part 2: proposed new tests, expect from the reader solution, and the planted one')
props = [
    ("count_varied_windows(['a', 'b', 'b', 'c'], 3)", 'count_varied_windows', mine_b.count_varied_windows, varied_first_last),
    ("count_varied_windows([1, 2, 2, 3, 4, 5, 5, 6], 4)", 'count_varied_windows', mine_b.count_varied_windows, varied_first_last),
    ("(lambda b: (b.__setitem__(50000, 49990), count_varied_windows(b, 30000))[1])(list(range(100000)))", 'count_varied_windows', mine_b.count_varied_windows, varied_first_last),
    ("widest_spacing(list(range(50000)) + [10 ** 9 - i for i in range(50000)], 3)", 'widest_spacing', mine_b.widest_spacing, None),
    ("net_tape([5, 1, -2])", 'net_tape', mine_b.net_tape, net_fifo),
    ("net_tape([-2, -3, 4])", 'net_tape', mine_b.net_tape, net_merge),
    ("closest_pair_gap([1, 5, 5], 10)", 'closest_pair_gap', mine_b.closest_pair_gap, hedge_dedupe),
    ("flattest_stretch([5, 9, -12, 4])", 'flattest_stretch', mine_a.flattest_stretch, flattest_min_or_total),
]
for call, fn, good, wrong in props:
    want = eval(call, {fn: good})
    line = f'  {call[:80]:80s} -> {want!r}'
    if wrong is not None:
        line += f'   planted gives {eval(call, {fn: wrong})!r}'
    print(line)

# timing of the kiosk walk-down on the proposed large test (stopped after 5 s)
import signal


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)
signal.alarm(5)
t0 = time.time()
try:
    kiosk_walk_down(list(range(50000)) + [10 ** 9 - i for i in range(50000)], 3)
    print(f'  kiosk walk-down on the proposed test finished in {time.time() - t0:.1f}s')
except TO:
    print('  kiosk walk-down on the proposed test: still running after 5 s natively')
finally:
    signal.alarm(0)
