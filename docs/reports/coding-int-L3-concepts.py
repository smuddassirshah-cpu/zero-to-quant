#!/usr/bin/env python3
"""Concept checks for coding-int level 3 (blind concept audit, 6 Nov 2026).

Run from the repo root: python3 -I docs/reports/coding-int-L3-concepts.py
Exit 0 when every check passes. A check that encodes a content claim the
audit found wrong stays failing until the content is fixed (brief step 4).

Covers l11 to l14, review-3 and homework-3: every Python and C++ code widget
(model solution passes its hidden tests, the untouched starter fails at least
one), and the stated traces, counts, invariants and complexity claims, by
brute force, operation counters or direct computation. No timing is used.
"""
import bisect
import heapq
import json
import math
import os
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, deque

ROOT = pathlib.Path(__file__).resolve().parents[2]
COURSE = ROOT / 'app' / 'content' / 'courses' / 'coding-int'
FAILS = []


def check(cond, name):
    print(('ok   ' if cond else 'FAIL ') + name)
    if not cond:
        FAILS.append(name)


def load(name):
    return json.loads((COURSE / f'{name}.json').read_text())


def code_widgets(doc):
    out = []

    def add(path, obj):
        w = obj.get('widget')
        if w and w.get('kind') == 'code':
            out.append((path, w))
        for k, p in enumerate(obj.get('parts', []) or []):
            w = p.get('widget')
            if w and w.get('kind') == 'code':
                out.append((f'{path}.parts[{k}]', w))

    for i, s in enumerate(doc.get('screens', [])):
        add(f'screens[{i}]', s)
    for key in ('quiz', 'items'):
        for i, it in enumerate(doc.get(key, [])):
            add(f'{key}[{i}]', it)
    return out


def _close(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    try:
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
    except TypeError:
        return a == b


def run_py(widget, code):
    """Run `code` against the widget's hidden tests as the engine does. Returns one bool per test."""
    tests = widget['tests']
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    try:
        for name, rel in (widget.get('data') or {}).items():
            shutil.copy(ROOT / 'app' / rel, name)
        ns = {'__learner_source__': code}
        src = widget.get('prelude', '') + '\n' + code + '\n' + widget.get('postlude', '')
        try:
            exec(src, ns)
        except Exception:
            return [False] * len(tests)
        res = []
        for t in tests:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns)
                        res.append(False)
                    except Exception as e:
                        res.append(isinstance(e, eval(t['expect'], ns)))
                    continue
                val = eval(t['call'], ns)
                exp = eval(t['expect'], ns)
                res.append(_close(val, exp) if t.get('compare') == 'isclose' else val == exp)
            except Exception:
                res.append(False)
        return res
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


CPP_PRINT = r'''
#include <iostream>
#include <string>
#include <vector>
static void pj(int v) { std::cout << v; }
static void pj(long long v) { std::cout << v; }
static void pj(const std::string& s) { std::cout << '"' << s << '"'; }
template <class T> static void pj(const std::vector<T>& v) {
    std::cout << '[';
    for (size_t i = 0; i < v.size(); ++i) { if (i) std::cout << ','; pj(v[i]); }
    std::cout << ']';
}
'''


def cpp_lit(value, typ):
    if typ is None:
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (int, float)):
            return repr(value)
        if isinstance(value, str):
            return json.dumps(value)
        return '{' + ','.join(cpp_lit(v, None) for v in value) + '}'
    if typ.startswith('std::vector<'):
        inner = typ[len('std::vector<'):-1]
        return typ + '{' + ','.join(cpp_lit(v, inner) for v in value) + '}'
    if typ == 'std::string':
        return json.dumps(value)
    return str(value)


def cpp_run_source(src, timeout=120):
    """Compile and run a C++17 program; returns stdout or None on a compile error."""
    tmp = tempfile.mkdtemp()
    try:
        p = pathlib.Path(tmp) / 'main.cpp'
        p.write_text(src)
        c = subprocess.run(['g++', '-std=c++17', '-O1', '-o', tmp + '/a.out', str(p)],
                           capture_output=True, text=True)
        if c.returncode != 0:
            return None
        r = subprocess.run([tmp + '/a.out'], capture_output=True, text=True, timeout=timeout)
        return r.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_cpp(widget, code, extra_tests=None):
    """Run C++ `code` against the widget's tests (function mode) with g++. Returns one bool per test."""
    tests = list(widget['tests']) + list(extra_tests or [])
    main = ['int main() {']
    for k, t in enumerate(tests):
        body = []
        if t.get('setup'):
            body.append(t['setup'])
        call = t['call']
        if 'args' in t or 'types' in t:
            types = t.get('types') or [None] * len(t.get('args', []))
            args = t.get('args', [[] for _ in types])
            call = call + '(' + ', '.join(cpp_lit(a, ty) for a, ty in zip(args, types)) + ')'
        body.append(f'std::cout << {k} << " "; pj({call}); std::cout << "\\n";')
        main.append('{' + '\n'.join(body) + '}')
    main.append('return 0; }')
    src = code + '\n' + widget.get('postlude', '') + '\n' + CPP_PRINT + '\n'.join(main)
    out = cpp_run_source(src)
    if out is None:
        return [False] * len(tests)
    got = {}
    for line in out.splitlines():
        k, _, rest = line.partition(' ')
        try:
            got[int(k)] = json.loads(rest)
        except ValueError:
            pass
    return [k in got and got[k] == t.get('expect', []) for k, t in enumerate(tests)]


def check_code(doc, label):
    for path, w in code_widgets(doc):
        runner = run_cpp if w.get('language') == 'cpp' else run_py
        sol = runner(w, w['solution'])
        st = runner(w, w['starter'])
        check(all(sol), f'{label} {path}: model solution passes all {len(sol)} hidden tests')
        check(not all(st), f'{label} {path}: untouched starter fails at least one hidden test')


def widget(doc, path):
    key, idx = path[:-1].split('[')
    return doc[key][int(idx)]['widget']


def ns_of(w, code=None):
    ns = {}
    exec(w.get('prelude', '') + '\n' + (code or w['solution']) + '\n' + w.get('postlude', ''), ns)
    return ns


# ---------------------------------------------------------------- load
from collections import OrderedDict
L11, L12, L13, L14 = (load(n) for n in ('l11-lru-cache', 'l12-file-system', 'l13-requirements-change', 'l14-rate-limiter'))
R3, H3 = load('review-3'), load('homework-3')
random.seed(20261106)

print('# code widgets: solution passes, starter fails')
for doc, label in ((L11, 'l11'), (L12, 'l12'), (L13, 'l13'), (L14, 'l14'), (R3, 'review-3'), (H3, 'homework-3')):
    check_code(doc, label)

# ---------------------------------------------------------------- l11 LRU and TTL caches
print('# l11 LRU cache')
LRUCache = ns_of(widget(L11, 'screens[2]'))['LRUCache']
TTLCache = ns_of(widget(L11, 'screens[6]'))['TTLCache']
LFUCache = ns_of(widget(H3, 'items[1]'))['LFUCache']


class LRURef:
    def __init__(self, cap):
        self.cap, self.d = cap, OrderedDict()

    def get(self, k):
        if k not in self.d:
            return -1
        self.d.move_to_end(k)
        return self.d[k]

    def put(self, k, v):
        if k in self.d:
            self.d.move_to_end(k)
        self.d[k] = v
        if len(self.d) > self.cap:
            self.d.popitem(last=False)

    def keys_recent_first(self):
        return list(self.d)[::-1]


def lru_keys(c):
    out, n = [], c.head.next
    while n is not c.tail:
        out.append(n.key)
        n = n.next
    return out


ok = True
for _ in range(200):
    cap = random.randint(1, 4)
    a, b = LRUCache(cap), LRURef(cap)
    for _ in range(30):
        k = random.randint(1, 6)
        if random.random() < 0.5:
            v = random.randint(0, 99)
            a.put(k, v)
            b.put(k, v)
        else:
            ok &= a.get(k) == b.get(k)
        ok &= lru_keys(a) == b.keys_recent_first()
check(ok, 'l11 s2: the dict-plus-list cache matches an OrderedDict reference (values and recency order) on 200 random runs')
c = LRUCache(1)
c.put(2, 1)
r = [c.get(2)]
c.put(3, 2)
r += [c.get(2), c.get(3)]
check(r == [1, -1, 2] and r.count(-1) == 1, 'l11 s3: capacity 1 gives 1, -1, 2: one miss')
c = LRUCache(2)
c.put(1, 10)
c.put(2, 20)
c.put(2, 21)
check(c.get(1) == 10 and c.get(2) == 21, 'l11 s5: a put of a stored key on a full cache updates it and evicts nothing')
c = LRUCache(2)
for k, v in ((7, 70), (9, 90)):
    c.put(k, v)
c.get(7)
c.put(4, 40)
check(c.get(9) == -1 and c.get(7) == 70, 'l11 q0: after get 7, put 4 evicts key 9')
c = LRUCache(1)
c.put(4, 8)
c.put(4, 9)
check(c.get(4) == 9, 'l11 q2: the second put updates the value to 9')
c = LRUCache(1000)
for i in range(100000):
    c.put(i, i)
check(sum(c.get(i) for i in range(99000, 100000)) + c.get(0) == 99499499 == 1000 * (99000 + 99999) // 2 - 1, 'l11 s10: 99,499,500 - 1')
out = cpp_run_source(r'''
#include <list>
#include <iostream>
int main() {
    std::list<int> l = {1, 2, 3, 4};
    auto it = l.begin(); ++it; ++it;           // iterator to 3
    l.splice(l.begin(), l, it);                // move 3 to the front
    l.erase(l.begin());                        // erase the front, now 3: {1, 2, 4}
    std::cout << l.size();
    std::list<int> m = {1, 2, 3, 4};
    auto it3 = m.begin(); ++it3; ++it3;        // 3
    m.erase(m.begin());                        // erase another element
    m.splice(m.begin(), m, it3);               // it3 still valid
    for (int x : m) std::cout << x;
    return 0;
}
''')
check(out == '3' + '324', 'l11 s4: std::list iterators stay valid when other nodes are erased or spliced')


class TTLRef:
    def __init__(self, cap, ttl):
        self.cap, self.ttl, self.d = cap, ttl, OrderedDict()   # key -> (value, touched), last = most recent

    def purge(self, now):
        for k in [k for k, (v, t) in self.d.items() if now - t >= self.ttl]:
            del self.d[k]

    def get(self, k, now):
        self.purge(now)
        if k not in self.d:
            return -1
        v, _ = self.d.pop(k)
        self.d[k] = (v, now)
        return v

    def put(self, k, v, now):
        self.purge(now)
        if k in self.d:
            del self.d[k]
        elif len(self.d) == self.cap:
            self.d.popitem(last=False)
        self.d[k] = (v, now)


def ttl_touched(c):
    out, n = [], c.head.next
    while n is not c.tail:
        out.append(n.touched)
        n = n.next
    return out


ok = mono = True
for _ in range(200):
    cap, ttl = random.randint(1, 3), random.randint(1, 5)
    a, b = TTLCache(cap, ttl), TTLRef(cap, ttl)
    now = 0
    for _ in range(30):
        now += random.randint(0, 2)
        k = random.randint(1, 5)
        if random.random() < 0.5:
            v = random.randint(0, 99)
            a.put(k, v, now)
            b.put(k, v, now)
        else:
            ok &= a.get(k, now) == b.get(k, now)
        ts = ttl_touched(a)
        mono &= all(x >= y for x, y in zip(ts, ts[1:]))
        ok &= set(lru_keys(a)) == set(b.d)
check(ok, 'l11 s6: the TTL cache matches a reference that purges every expired entry (200 random runs, clock non-decreasing)')
check(mono, 'l11 s7: times of last use never rise from head to tail, so expired entries form a suffix')
c = TTLCache(2, 5)
c.put(1, 10, 0)
check(c.get(1, 5) == -1, 'l11 s6 test 2: an age equal to the ttl counts as expired')
a, b = TTLCache(2, 4), TTLCache(2, 4)
a.put(1, 1, 3)
b.put(1, 1, 3)
check(a.get(1, 6) == 1 and a.get(1, 10) == -1 and b.get(1, 6) == 1 and b.get(1, 9) == 1,
      'l11 q3: read at 6 refreshes; the entry is still there at 9 and gone at 10')
c = LRUCache(1000)
for k in range(50):
    c.put(k, k)
for _ in range(20):
    for k in range(50):
        c.get(k)
for k in range(10000, 15000):
    c.put(k, k)
lfu = LFUCache(1000)
for k in range(50):
    lfu.put(k, k)
for _ in range(20):
    for k in range(50):
        lfu.get(k)
for k in range(10000, 15000):
    lfu.put(k, k)
check(all(c.get(k) == -1 for k in range(50)) and all(lfu.get(k) == k for k in range(50)),
      'l11 s9: a scan of 5,000 cold keys evicts every hot key under LRU; LFU keeps all 50')

print('# review-3 caches')
c = LRUCache(3)
r = []
for op in (('p', 2), ('p', 4), ('p', 6), ('g', 2), ('p', 8), ('g', 4), ('g', 6), ('p', 10), ('g', 2), ('g', 8)):
    if op[0] == 'p':
        c.put(op[1], op[1])
    else:
        r.append(c.get(op[1]))
check(r == [2, -1, 6, -1, 8] and sum(r) == 14, 'r3 i0: gets 2, -1, 6, -1, 8 sum to 14')
c = LRUCache(3)
for k in (12, 15, 11):
    c.put(k, k)
c.get(12)
c.put(14, 14)
check(c.get(15) == -1 and lru_keys(c) == [14, 12, 11], 'r3 i1: key 15 is evicted')
c = TTLCache(2, 3)
c.put(1, 1, 0)
r = [c.get(1, t) for t in (2, 5, 6, 9)]
check(r == [1, -1, -1, -1], 'r3 i2: the get at 2 hits; 5, 6 and 9 miss')

# ---------------------------------------------------------------- l12 file system
print('# l12 file system')
FileSystem = ns_of(widget(L12, 'screens[7]'))['FileSystem']
check('/'.split('/') == ['', ''] and '/a//b'.split('/') == ['', 'a', '', 'b'], 'l12 s5 and q0: split keeps empty names')
fs = FileSystem()
fs.mkdir('/a/b/c')
fs.write('/a/b/c/d.txt', 'hello')
check(fs.ls('/a') == ['b'] and fs.ls('/') == ['a'] and fs.ls('/a/b/c/d.txt') == ['d.txt'], 'l12 s0 and s2: ls lists direct children; ls of a file names the file')


def folder_count(n):
    return sum(1 + folder_count(c) for c in n.children.values() if c.content is None)


fs = FileSystem()
fs.mkdir('/a/b/c')
check(folder_count(fs.root) == 3, 'l12 s1: mkdir of /a/b/c makes three folders')
fs = FileSystem()
fs.write('/n/x.txt', 'hello')
fs.write('/n/x.txt', ' world')
check(fs.read('/n/x.txt') == 'hello world', 'l12 s3: write creates and appends')
fs = FileSystem()
for p, t in (('/logs/a.txt', 'abcd'), ('/logs/old/b.txt', 'xy'), ('/logs/c.txt', 'abcdef')):
    fs.write(p, t)
check(fs.size('/logs') == 12 and fs.size('/logs/old') == 2, 'l12 s6: size(/logs) = 12, size(/logs/old) = 2')
fs = FileSystem()
for p, t in (('/s/a', 'x' * 7), ('/s/t/b', 'x' * 3), ('/s/t/c', 'x' * 10)):
    fs.write(p, t)
check(fs.size('/s/t') == 13 and fs.size('/s') == 20, 'l12 q3: size(/s/t) = 13')
fs = FileSystem()
fs.mkdir('/p/q')
fs.write('/p/q/r.txt', 'hi')
fs.mkdir('/p/q')
check(fs.ls('/p/q') == ['r.txt'], 'l12 q2: a repeated mkdir changes nothing')
fs = FileSystem()
for p, t in (('/var/a/one.txt', '123456'), ('/var/a/two.txt', '12345678901'), ('/var/b.txt', '1234')):
    fs.write(p, t)
check(fs.size('/var') == 21 and fs.size('/var/a') == 17, 'r3 i3: size(/var) = 21')
fs = FileSystem()
fs.mkdir('/y')
fs.mkdir('/x')
fs.write('/m.txt', '9')
fs.write('/y/k.txt', '9')
check(fs.ls('/') == ['m.txt', 'x', 'y'] and sorted(['y', 'x', 'm.txt']) == ['m.txt', 'x', 'y'], 'r3 i4: ls(/) is sorted: m.txt, x, y')

# ---------------------------------------------------------------- l13 ledger
print('# l13 ledger')
Ledger2 = ns_of(widget(L13, 'screens[3]'))['Ledger']
Ledger3 = ns_of(widget(L13, 'screens[6]'))['Ledger']
check((100 * 10 + 100 * 12) / 200 == 11 and 150 * (13 - 11) == 300, 'l13 s2: average 11, the sale realises 300')
L = Ledger3(method='fifo')
L.trade('ABC', 100, 10)
L.trade('ABC', 100, 12)
L.trade('ABC', -150, 13)
check(L.realised('ABC') == 350 and L.avg_cost('ABC') == 12.0 and L.position('ABC') == 50, 'l13 s5: FIFO realises 350; 50 shares left at 12')


def required_price(self, symbol, qty, price):
    pass


def kw_only(self, symbol, qty, *, price):
    pass


def raises_type_error(f, *a):
    try:
        f(None, *a)
        return False
    except TypeError:
        return True


check(raises_type_error(required_price, 'ABC', 100) and raises_type_error(kw_only, 'ABC', 5)
      and not raises_type_error(lambda self, symbol, qty, price=0: None, 'ABC', 5),
      'l13 s4 and q3: a required price (positional or keyword-only) raises TypeError on the old two-argument call; a default does not')


def realised_both(trades):
    a, f = Ledger3(), Ledger3(method='fifo')
    for q, p in trades:
        a.trade('S', q, p)
        f.trade('S', q, p)
    return a.realised('S'), f.realised('S')


check(_close(list(realised_both([(20, 30), (-5, 34), (10, 36), (-15, 33)])), [29, 65]), 'l13 s10: average cost realises 29, FIFO 65 (difference 36)')
check(abs(((15 * 30 + 10 * 36) / 25) - 32.4) < 1e-9, 'l13 s10: the second average is 32.4')
check((40 * 9 + 60 * 14) / 100 == 12, 'l13 q1: average 12')
L = Ledger3(method='fifo')
L.trade('ABC', 10, 8)
L.trade('ABC', 10, 11)
L.trade('ABC', -5, 12)
check(L.realised('ABC') == 20, 'l13 q2: FIFO realises 20')
check(_close(list(realised_both([(200, 20), (100, 23), (-250, 25)])), [1000, 1100]), 'r3 i5: FIFO 1,100; average cost 1,000')
check(_close(list(realised_both([(8, 60), (-3, 64), (15, 52), (-10, 58)])), [52, 32]), 'h3 i0: average cost 52, FIFO 32, gap 20')
ok = True
for _ in range(200):
    held, trades = 0, []
    for _ in range(random.randint(1, 6)):
        q = random.randint(1, 9)
        trades.append((q, random.randint(5, 30)))
        held += q
        if held and random.random() < 0.5:
            s = random.randint(1, held)
            trades.append((-s, random.randint(5, 30)))
            held -= s
    if held:
        trades.append((-held, random.randint(5, 30)))
    a, f = realised_both(trades)
    cash = sum(-q * p for q, p in trades)
    ok &= abs(a - f) < 1e-6 and abs(a - cash) < 1e-6
check(ok, 'h3 i0 p2: once every share is sold, average cost and FIFO realise the same total, the net cash (200 random ledgers)')

# ---------------------------------------------------------------- l14 rate limiters
print('# l14 rate limiters')
RateLimiter = ns_of(widget(L14, 'screens[3]'))['RateLimiter']
TokenBucket = ns_of(widget(L14, 'screens[6]'))['TokenBucket']


def log_fresh(limit, window, accepted, t):
    r = RateLimiter(limit, window)
    for s in accepted:
        assert r.allow('u', s)
    return r.allow('u', t)


check([log_fresh(2, 10, [5, 6], t) for t in (14, 15, 16)] == [False, True, True], 'l14 s0: against the log 5, 6 the requests at 15 and 16 are accepted, 14 is refused')
check([log_fresh(1, 10, [6], t) for t in (15, 16)] == [False, True], 'l14 s1: the time 6 stops counting at 16')


def run_log(limit, window, times):
    r = RateLimiter(limit, window)
    return [r.allow('u', t) for t in times]


check(run_log(2, 3, [0, 1, 2, 3, 4, 5]) == [True, True, False, True, True, False], 'l14 s2: 0, 1, 3, 4 accepted')
check(run_log(2, 10, [0, 1, 5, 10, 11]) == [True, True, False, True, True], 'l14 s4: 0, 1, 10, 11 accepted; the refused 5 leaves no mark')


def run_log_recording(limit, window, times):
    q, out = deque(), []
    for t in times:
        q.append(t)
        while q and q[0] <= t - window:
            q.popleft()
        out.append(len(q) <= limit)
    return out


check(run_log_recording(2, 10, [0, 1, 5, 10, 11]) == [True, True, False, False, False], 'l14 s4 o1.why: recording refused requests locks the client out at 10 and 11')


def fixed_window(limit, block, times):
    counts = Counter()
    out = []
    for t in times:
        b = t // block
        counts[b] += 1
        out.append(counts[b] <= limit)
    return out


check(sum(fixed_window(40, 30, [29] * 40 + [30] * 40)) == 80 and sum(run_log(40, 30, [29] * 40 + [30] * 40)) == 40,
      'l14 s5: a fixed counter admits 80, a sliding log 40')
check(sum(fixed_window(100, 60, [59] * 100 + [60] * 100)) == 200 and sum(run_log(100, 60, [59] * 100 + [60] * 100)) == 100,
      'h3 i4 and h3 i3 model: 200 against 100 at the minute boundary')


def brute_log(limit, window, calls):
    accepted, out = {}, []
    for u, t in calls:
        n = sum(1 for s in accepted.get(u, []) if s > t - window)
        if n < limit:
            accepted.setdefault(u, []).append(t)
            out.append(True)
        else:
            out.append(False)
    return out


ok = True
for _ in range(300):
    limit, window = random.randint(1, 4), random.randint(1, 6)
    calls, t = [], 0
    for _ in range(random.randint(1, 20)):
        t += random.randint(0, 2)
        calls.append((random.choice('ab'), t))
    r = RateLimiter(limit, window)
    ok &= [r.allow(u, s) for u, s in calls] == brute_log(limit, window, calls)
check(ok, 'l14 s3: the deque limiter equals a count of accepted times above t - w (300 random runs, two users)')
calls = [('a', t // 3) for t in range(60000)]
r6 = RateLimiter(5, 100)
check(sum(brute_log(5, 100, calls[:6000])) == 100 and sum(r6.allow(u, t) for u, t in calls) == 1000, 'l14 s3 test 6: 5 per 100 seconds gives 1,000')


def bucket_ref(capacity, rate, times):
    tokens, last, out = float(capacity), 0, []
    for t in times:
        tokens = min(capacity, tokens + (t - last) * rate)
        last = t
        if tokens >= 1:
            tokens -= 1
            out.append(True)
        else:
            out.append(False)
    return out


def run_bucket(capacity, rate, times):
    b = TokenBucket(capacity, rate)
    return [b.allow(t) for t in times]


check(sum(run_bucket(2, 2, [0, 0, 0, 1, 1, 1])) == 4, 'l14 s7: 2 + 2 = 4 accepted')
check(sum(run_bucket(10, 1, [t // 4 for t in range(200000)])) == 50009 == 12 + 49997, 'l14 s6 test 6: 50,009')
b = TokenBucket(5, 1)
for _ in range(5):
    b.allow(0)
b.allow(3)
check(abs(b.tokens - 2) < 1e-9, 'l14 q2: an emptied bucket holds 3 tokens at time 3 (2 after the request spends one)')
check(sum(run_bucket(4, 2, [0, 0, 0, 0, 0, 1, 1, 1, 2, 9])) == 8 and run_bucket(4, 2, [0, 0, 0, 0, 0, 1, 1, 1, 2, 9]) == [True] * 4 + [False, True, True, False, True, True],
      'r3 i8: 4 + 2 + 1 + 1 = 8 accepted')
check(run_log(3, 7, [0, 1, 2, 3, 4, 7, 8]) == [True, True, True, False, False, True, True], 'r3 i7: five accepted')
check(log_fresh(1, 4, [6], 10) is True and log_fresh(1, 5, [0], 5) is True and run_log(1, 5, [0, 2, 5]) == [True, False, True],
      'l14 q0 and q1: at the cut-off the old time has left; a refused request leaves no mark')
ok = True
for _ in range(200):
    cap, rate = random.randint(1, 5), random.choice([0, 0.5, 1, 2])
    times, t = [], 0
    for _ in range(random.randint(1, 15)):
        t += random.randint(0, 3)
        times.append(t)
    ok &= run_bucket(cap, rate, times) == bucket_ref(cap, rate, times)
check(ok, 'l14 s6: the lazy-refill bucket equals a reference on 200 random request streams')

# ---------------------------------------------------------------- homework-3 LFU and hit counter
print('# homework-3')


class LFURef:
    def __init__(self, cap):
        self.cap, self.d, self.clock = cap, {}, 0   # key -> [value, count, last]

    def touch(self, k):
        self.clock += 1
        self.d[k][1] += 1
        self.d[k][2] = self.clock

    def get(self, k):
        if k not in self.d:
            return -1
        self.touch(k)
        return self.d[k][0]

    def put(self, k, v):
        if self.cap == 0:
            return
        if k in self.d:
            self.d[k][0] = v
            self.touch(k)
            return
        if len(self.d) == self.cap:
            victim = min(self.d, key=lambda key: (self.d[key][1], self.d[key][2]))
            del self.d[victim]
        self.clock += 1
        self.d[k] = [v, 1, self.clock]


ok = True
for _ in range(300):
    cap = random.randint(0, 3)
    a, b = LFUCache(cap), LFURef(cap)
    for _ in range(30):
        k = random.randint(1, 5)
        if random.random() < 0.5:
            v = random.randint(0, 99)
            a.put(k, v)
            b.put(k, v)
        else:
            ok &= a.get(k) == b.get(k)
        ok &= set(a.vals) == set(b.d)
check(ok, 'h3 i1: the bucket LFU matches a reference that evicts the (count, last use) minimum (300 random runs)')
c = LFUCache(2)
r = []
for op in (('p', 1), ('p', 2), ('g', 1), ('p', 3), ('g', 2), ('g', 3), ('p', 4), ('g', 1), ('g', 3), ('g', 4)):
    if op[0] == 'p':
        c.put(op[1], op[1])
    else:
        r.append(c.get(op[1]))
check(r == [1, -1, 3, -1, 3, 4] and sum(r) == 9, 'h3 i7: gets 1, -1, 3, -1, 3, 4 sum to 9')
HitCounter = ns_of(widget(H3, 'items[2]'))['HitCounter']
ok = True
for _ in range(300):
    h, hits, t = HitCounter(), [], 0
    for _ in range(random.randint(1, 40)):
        t += random.choice([0, 0, 1, 2, 150, 299, 300, 301])
        if random.random() < 0.6:
            h.hit(t)
            hits.append(t)
        else:
            ok &= h.count(t) == sum(1 for s in hits if t - 300 < s <= t)
check(ok, 'h3 i2: the 300-slot ring equals a list of every hit on 300 random non-decreasing streams')
check(len(HitCounter().times) == 300 and len(HitCounter().counts) == 300, 'r3 i9: the ring holds 300 slots of two numbers')

print()
print(f'{len(FAILS)} failures')
for f in FAILS:
    print('  -', f)
sys.exit(1 if FAILS else 0)
