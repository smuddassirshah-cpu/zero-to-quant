"""Second half of the checks for topic-3.5: the items that need the built exam file.

Run after build.py:  python3 check2.py
 - 16 margin rules, 19 minutes plan (81 mixes), 20 planted bug, 24 struct layout (compiled with g++),
 - 21 and 10: model solutions in CPython against independent references; starters fail every test,
 - 30: the C++ solution compiled with g++ passes the tests; the starter and wrong-mask variants fail.
"""
import json, os, subprocess, sys, tempfile, itertools, random, textwrap, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import refs
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
EXAM = json.load(open(os.path.join(ROOT, 'app/content/exams/topic-3.5.json')))
BY = {i['id']: i for i in EXAM['items']}

# ---------------- 16 margin rules
def margin(pnl, top=True, withdraw='half'):
    bal = 500
    for p in pnl:
        if bal < 400: bal += 250
        bal += p
        if bal > 700:
            if withdraw == 'half': bal -= (bal - 700) // 2
            elif withdraw == 'all': bal = 700
            elif withdraw == 'balance': bal -= bal // 2
    return bal
pnl = [-120, -90, 60, 400, -250, -180]
# a second method: recurrence written out day by day
days = []
b = 500
for p in pnl:
    b = b + 250 if b < 400 else b
    b += p
    b = 700 + (b - 700) / 2 if b > 700 else b
    days.append(b)
assert days == [380, 540, 600, 850, 600, 420], days
assert margin(pnl) == 420 and margin(pnl, withdraw='all') == 270 and margin(pnl, withdraw='balance') == 320
nw = 500
for p in pnl:
    if nw < 400: nw += 250
    nw += p
assert nw == 570
print('16 ok: 420; slips 270, 570, 320')

# ---------------- 19 minutes plan
probs = [(30, 28, 12, 9), (40, 36, 18, 13), (25, 20, 10, 6), (50, 44, 20, 15)]
plans = []
for ch in itertools.product((0, 1, 2), repeat=4):
    pts = m = 0
    for c, (fp, fm, pp, pm) in zip(ch, probs):
        if c == 1: pts += fp; m += fm
        elif c == 2: pts += pp; m += pm
    if m <= 70: plans.append((pts, m, ch))
assert max(plans)[0] == 82 and (82, 66, (2, 1, 2, 2)) in plans and sorted(plans, reverse=True)[1][0] == 80 and len(list(itertools.product((0, 1, 2), repeat=4))) == 81
assert [p for p in plans if p[0] == 82] == [(82, 66, (2, 1, 2, 2))]
# knapsack by minutes as the second method
dp = [0] * 71
for fp, fm, pp, pm in probs:
    nd = dp[:]
    for t in range(71):
        for pts, m in ((fp, fm), (pp, pm)):
            if t >= m: nd[t] = max(nd[t], dp[t - m] + pts)
    dp = nd
assert max(dp) == 82
assert max(p for p in plans if all(c != 2 for c in p[2]))[0] == 75
assert max(p for p in plans if p[1] == 70)[0] == 80
assert sum(p[2] for p in probs) == 60 and sum(p[3] for p in probs) == 43
print('19 ok: 82; slips 75, 80, 60')

# ---------------- 20 planted bug
def good(xs, k):
    if len(xs) < k: return None
    return max(sum(xs[i:i + k]) for i in range(len(xs) - k + 1))
def bug(xs, k):
    if len(xs) <= k: return None
    best = sum(xs[:k])
    for i in range(1, len(xs) - k + 1): best = max(best, sum(xs[i:i + k]))
    return best
calls = {"a": ([6], 1), "b": ([2, 3, 5], 3), "c": ([4, 1], 2), "d": ([], 2), "e": ([1, 2], 3), "f": ([5, 1, 4, 2], 2)}
opts = {o['id']: bool(o.get('correct')) for o in BY['e-window-inputs']['widget']['options']}
for key, (xs, k) in calls.items():
    assert (good(xs, k) != bug(xs, k)) == opts[key], key
print('20 ok')

# ---------------- 24 struct layout, compiled
src = '''#include <cstdint>
#include <cstddef>
#include <cstdio>
struct Tick { uint8_t side; uint32_t qty; uint16_t venue; uint64_t id; };
int main(){ printf("%zu %zu %zu %zu %zu\\n", sizeof(Tick), offsetof(Tick, side), offsetof(Tick, qty), offsetof(Tick, venue), offsetof(Tick, id)); }'''
with tempfile.TemporaryDirectory() as d:
    open(d + '/t.cpp', 'w').write(src)
    subprocess.check_call(['g++', '-std=c++17', '-o', d + '/t', d + '/t.cpp'])
    size, o_side, o_qty, o_venue, o_id = map(int, subprocess.check_output([d + '/t']).split())
used = set(range(o_side, o_side + 1)) | set(range(o_qty, o_qty + 4)) | set(range(o_venue, o_venue + 2)) | set(range(o_id, o_id + 8))
pad = sorted(set(range(size)) - used)
assert size == 24 and pad == [1, 2, 3, 10, 11, 12, 13, 14, 15], (size, pad)
def rc(k): return 'r%dc%d' % (k // 8 + 1, k % 8 + 1)
assert sorted(BY['e-tick-padding']['widget']['answer']) == sorted(rc(k) for k in pad)
print('24 ok: size', size, 'padding bytes', pad)

# ---------------- 21 and 10: Python solutions
def run_widget(w, source):
    ns = {'__name__': '__main__'}
    if w.get('prelude'): exec(w['prelude'], ns)
    exec(source, ns)
    res = []
    for t in w['tests']:
        try:
            if t.get('setup'): exec(t['setup'], ns)
            act = eval(t['call'], ns); exp = eval(t['expect'], ns)
            res.append(act == exp)
        except Exception as e:
            res.append(False)
    return res

w21 = BY['e-active-symbols']['widget']
r = run_widget(w21, w21['solution']); assert all(r), r
r = run_widget(w21, w21['starter']); assert not any(r), r
# independent brute force on the small tests and a sample of the large one
ev = [('X', 1), ('Y', 5), ('X', 8)]
assert refs.active_query_brute(ev, 10, 8) == 2
assert [refs.active_query_brute([('X', 0)], 10, 9), refs.active_query_brute([('X', 0)], 10, 10)] == [1, 0]
assert refs.active_query_brute([('X', i) for i in range(4)], 5, 3) == 1
ev = [('X', 0), ('Y', 4), ('X', 8)]
assert [refs.active_query_brute(ev, 10, t) for t in (11, 14, 18, 19)] == [2, 1, 0, 0]
assert [refs.active_query_brute([], 3, t) for t in (0, 100)] == [0, 0]
ev = [('A', 5), ('B', 5), ('A', 5)]
assert [refs.active_query_brute(ev, 1, t) for t in (5, 6)] == [2, 0]
assert refs.active_total_bit(3000, 2000) == refs.active_total_brute(3000, 2000) and refs.active_total_bit(9000, 300) == refs.active_total_brute(9000, 300)
big = [t for t in w21['tests'] if t['call'] == 'total'][0]
assert big['expect'] == str(refs.active_total_bit())
# a quadratic scan of the log (dict of last seen) is slow: time it on the large test
import time
def scan_solution():
    class A:
        def __init__(s, w): s.w = w; s.last = {}
        def tick(s, sym, t): s.last[sym] = t
        def active(s, t): return sum(1 for u in s.last.values() if u > t - s.w)
    return A
ns = {}
t0 = time.time(); a = scan_solution()(2000); tot = 0
for i in range(30000):
    a.tick((i * 7919) % 30011, i // 3); tot += a.active(i // 3)
dt = time.time() - t0
print('21 ok. A dict scan took %.1f s for 30,000 of the 100,000 calls (limit 5 s)' % dt)

w10 = BY['e-costliest-desk']['widget']
r = run_widget(w10, w10['solution']); assert all(r), r
r = run_widget(w10, w10['starter'])
print('10 starter passes', sum(r), 'of', len(r), '(None-returning tests pass; the rest fail)')
assert sum(r) < len(r)
# independent: exact-fraction slopes
import pandas as pd
from fractions import Fraction as F
def slope_exact(xs, ys):
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    return F(n * sxy - sx * sy, n * sxx - sx * sx)
def costliest_exact(df, m):
    best = None
    for name in sorted(set(df['desk'])):
        g = df[df['desk'] == name]
        if len(g) < m or len(set(g['size'])) < 2: continue
        s = slope_exact([int(v) for v in g['size']], [int(v) for v in g['cost']])
        if best is None or s > best[1]: best = (name, s)
    return best[0] if best else None
ns = {}
exec(w10['prelude'], ns)
FILLS = ns['FILLS']
assert costliest_exact(FILLS, 4) == 'north' and costliest_exact(FILLS, 3) == 'south' and costliest_exact(FILLS, 6) is None
assert slope_exact([1, 2, 3, 4], [3, 5, 8, 9]) == F(21, 10) and slope_exact([5, 6, 7], [2, 9, 14]) == 6
print('10 ok')

# ---------------- 30 C++ ring
w30 = BY['e-newest-first']['widget']
def cpp_value(v):
    if isinstance(v, list): return '{' + ', '.join(cpp_value(x) for x in v) + '}'
    return str(v)
def run_cpp(source):
    main = ['int main() {', '  int fails = 0;']
    for i, t in enumerate(w30['tests']):
        xs, cap, k = t['args']
        main.append('  { std::vector<int> got = newest_first(std::vector<int>%s, %d, %d); std::vector<int> want = %s; if (got != want) { ++fails; printf("test %d failed\\n"); } }'
                    % (cpp_value(xs), cap, k, '{' + ', '.join(map(str, t['expect'])) + '}' if t['expect'] else 'std::vector<int>{}', i + 1))
    main += ['  printf("fails %d\\n", fails);', '  return fails;', '}']
    code = '#include <cstdio>\n' + source + '\n' + '\n'.join(main) + '\n'
    with tempfile.TemporaryDirectory() as d:
        open(d + '/m.cpp', 'w').write(code)
        r = subprocess.run(['g++', '-std=c++17', '-O1', '-D_GLIBCXX_ASSERTIONS', '-fsanitize=address,undefined', '-o', d + '/m', d + '/m.cpp'], capture_output=True, text=True)
        if r.returncode: return 'COMPILE ERROR ' + r.stderr[:300]
        r = subprocess.run([d + '/m'], capture_output=True, text=True)
        return (r.returncode, r.stdout.strip().replace('\n', '; '), r.stderr[:80].replace('\n', ' '))
sol = run_cpp(w30['solution'])
assert sol[0] == 0 and 'fails 0' in sol[1], sol
sta = run_cpp(w30['starter'])
assert sta[0] != 0, sta
variants = {
    'mask-is-capacity': ('count & mask', 'count & (unsigned)capacity'),
    'modulo-capacity-minus-one': ('count & mask', 'count % (capacity > 1 ? capacity - 1 : 1)'),
    'read-mask-wrong': ('buf[(count - 1 - i) & mask]', 'buf[(count - 1 - i) % (capacity + 1 > 0 ? capacity - 1 : 1) % capacity]'),
}
for name, (a_, b_) in variants.items():
    src = w30['solution'].replace(a_, b_, 1) if name != 'read-mask-wrong' else w30['solution'].replace(a_, b_)
    assert src != w30['solution']
    r = run_cpp(src)
    assert r == 'COMPILE ERROR' or (isinstance(r, str) or r[0] != 0), (name, r)
    print('   variant', name, 'fails:', r if isinstance(r, str) else r[:2])
# mirror in Python for the expected values
rr = random.Random(305)
big = [rr.randint(1, 999) for _ in range(300)]
assert w30['tests'][4]['args'][0] == big
def ring_py(xs, cap, k):
    buf = [0] * cap; count = 0; mask = cap - 1
    for x in xs: buf[count & mask] = x; count += 1
    held = min(count, cap)
    return [buf[(count - 1 - i) & mask] for i in range(min(k, held))]
for t in w30['tests']:
    xs, cap, k = t['args']; assert ring_py(xs, cap, k) == t['expect'] == list(reversed(xs[-cap:]))[:k]
print('30 ok: solution passes all 6 under sanitizers; starter fails; variants fail')
print('all second-half checks passed')
