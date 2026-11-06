"""Second route for app/content/exams/mock-oa-code-hard.json. Exits 1 on any failure.

Independent of mock-oa-code-hard_build.py. H1: a NumPy scan over every worker for each job. H2: Dijkstra from site 0
and Dijkstra on the reversed links to site n - 1, then the best of the plain route and every link made free
(d0[u] + dn[v]), which needs no state. H3: the C++ reference, starter and planted wrong versions are compiled with the
local g++ (-std=c++17 -O1) and run on every case; a NumPy DP over holdings and a 3 ** n brute force give the second
values. Every Python solution passes every hidden test and example in CPython; every starter and planted wrong version
fails at least one. Every number in every learner-visible string must be a stated input, a test count or an answer.
Uses app/tools/numbers_lib.py (check_wrongs, then report).
Run: python3 -I docs/briefs/mocks-scripts/mock-oa-code-hard_check.py
"""
import heapq
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from itertools import accumulate

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _NUM, normalise  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-oa-code-hard.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = {it['id']: it for it in doc['parts'][0]['items']}


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, note)


def run_py(src, case):
    g = {}
    exec(src, g)
    if case.get('setup'):
        exec(case['setup'], g)
    t0 = time.perf_counter()
    try:
        got = eval(case['call'], g)
    except Exception as e:  # noqa: BLE001
        return None, f'raised {type(e).__name__}', 0, g
    return got, repr(got)[:60], (time.perf_counter() - t0) * 1000, g


# ---------------------------------------------------------------- H1, route B: NumPy scan
def h1_numpy(k, jobs):
    end = np.zeros(k, dtype=np.int64)
    count = np.zeros(k, dtype=np.int64)
    last = 0
    for arrive, length in sorted(jobs):
        free = np.flatnonzero(end <= arrive)
        if free.size:
            w, start = int(free[0]), arrive
        else:
            w = int(np.argmin(end))          # argmin returns the first, so the lowest number on a tie
            start = int(end[w])
        end[w] = start + length
        count[w] += 1
        last = max(last, int(end[w]))
    if not jobs:
        return [0, 0]
    return [int(np.argmax(count)), last]  # argmax returns the first maximum: the lowest number


# ---------------------------------------------------------------- H2, route B: two plain Dijkstras, no state
def dijkstra(n, adj, src):
    d = [None] * n
    d[src] = 0
    pq = [(0, src)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != d[u]:
            continue
        for v, c in adj[u]:
            if d[v] is None or du + c < d[v]:
                d[v] = du + c
                heapq.heappush(pq, (du + c, v))
    return d


def h2_two_way(n, links):
    fwd = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v, c in links:
        fwd[u].append((v, c))
        rev[v].append((u, c))
    d0, dn = dijkstra(n, fwd, 0), dijkstra(n, rev, n - 1)
    cands = [d0[n - 1]] if d0[n - 1] is not None else []
    cands += [d0[u] + dn[v] for u, v, _ in links if d0[u] is not None and dn[v] is not None]
    return min(cands) if cands else -1


WRONG_PY = {
    'h1-busiest-worker': {
        'strict free': 'import heapq\ndef busiest_worker(k, jobs):\n    free = list(range(k)); busy = []; count = [0] * k; last = 0\n    for a, l in sorted(jobs):\n        while busy and busy[0][0] < a:\n            heapq.heappush(free, heapq.heappop(busy)[1])\n        if free:\n            w, s = heapq.heappop(free), a\n        else:\n            s, w = heapq.heappop(busy)\n        heapq.heappush(busy, (s + l, w)); count[w] += 1; last = max(last, s + l)\n    return [min(range(k), key=lambda w: (-count[w], w)), last] if jobs else [0, 0]\n',
        'end from arrival': 'import heapq\ndef busiest_worker(k, jobs):\n    free = list(range(k)); busy = []; count = [0] * k; last = 0\n    for a, l in sorted(jobs):\n        while busy and busy[0][0] <= a:\n            heapq.heappush(free, heapq.heappop(busy)[1])\n        if free:\n            w, s = heapq.heappop(free), a\n        else:\n            s, w = heapq.heappop(busy)\n        heapq.heappush(busy, (a + l, w)); count[w] += 1; last = max(last, a + l)\n    return [min(range(k), key=lambda w: (-count[w], w)), last] if jobs else [0, 0]\n',
        'waits for lowest number': 'def busiest_worker(k, jobs):\n    end = [0] * k; count = [0] * k; last = 0\n    for a, l in sorted(jobs):\n        free = [w for w in range(k) if end[w] <= a]\n        w = free[0] if free else 0\n        s = a if free else end[0]\n        end[w] = s + l; count[w] += 1; last = max(last, end[w])\n    return [min(range(k), key=lambda w: (-count[w], w)), last] if jobs else [0, 0]\n',
        'unsorted input': 'import heapq\ndef busiest_worker(k, jobs):\n    free = list(range(k)); busy = []; count = [0] * k; last = 0\n    for a, l in jobs:\n        while busy and busy[0][0] <= a:\n            heapq.heappush(free, heapq.heappop(busy)[1])\n        if free:\n            w, s = heapq.heappop(free), a\n        else:\n            s, w = heapq.heappop(busy)\n        heapq.heappush(busy, (s + l, w)); count[w] += 1; last = max(last, s + l)\n    return [min(range(k), key=lambda w: (-count[w], w)), last] if jobs else [0, 0]\n',
    },
    'h2-voucher-route': {
        'plain route minus dearest link': 'import heapq\ndef cheapest_with_voucher(n, links):\n    adj = [[] for _ in range(n)]\n    for u, v, c in links:\n        adj[u].append((v, c))\n    best = {0: (0, 0)}; pq = [(0, 0, 0)]; done = set()\n    while pq:\n        d, mx, u = heapq.heappop(pq)\n        if u in done:\n            continue\n        done.add(u)\n        if u == n - 1:\n            return d - mx\n        for v, c in adj[u]:\n            if v not in done and (v not in best or d + c < best[v][0]):\n                best[v] = (d + c, max(mx, c)); heapq.heappush(pq, (d + c, max(mx, c), v))\n    return -1\n',
        'voucher on every link': 'def cheapest_with_voucher(n, links):\n    seen = {0}; stack = [0]\n    while stack:\n        u = stack.pop()\n        for a, b, c in links:\n            if a == u and b not in seen:\n                seen.add(b); stack.append(b)\n    return 0 if n - 1 in seen else -1\n',
        'links both ways': 'import heapq\ndef cheapest_with_voucher(n, links):\n    adj = [[] for _ in range(n)]\n    for u, v, c in links:\n        adj[u].append((v, c)); adj[v].append((u, c))\n    best = [[float("inf")] * 2 for _ in range(n)]; best[0][0] = 0; pq = [(0, 0, 0)]\n    while pq:\n        d, u, s = heapq.heappop(pq)\n        if d > best[u][s]:\n            continue\n        if u == n - 1:\n            return d\n        for v, c in adj[u]:\n            if d + c < best[v][s]:\n                best[v][s] = d + c; heapq.heappush(pq, (d + c, v, s))\n            if not s and d < best[v][1]:\n                best[v][1] = d; heapq.heappush(pq, (d, v, 1))\n    return -1\n',
    },
}

for iid, second in (('h1-busiest-worker', None), ('h2-voucher-route', None)):
    w = items[iid]['widget']
    rec(w['language'] == 'python' and 3 <= len(w['tests']) <= 15, f'{iid}: Python, {len(w["tests"])} tests')
    rec(f'There are {len(w["tests"])} hidden tests.' in w['how'], f'{iid}: how line counts the tests')
    slow = 0
    for k, case in enumerate(w['examples'] + w['tests']):
        got, shown, ms, g = run_py(w['solution'], case)
        want = eval(case['expect'])
        slow = max(slow, ms)
        rec(got == want, f'{iid}: solution passes {case["call"][:60]}', '' if got == want else shown)
        # route B on the same inputs
        if iid == 'h1-busiest-worker':
            m = re.match(r'list\(busiest_worker\((\d+), (.*)\)\)$', case['call'])
            kk = int(m.group(1))
            jobs = g['J'] if m.group(2) == 'J' else json.loads(m.group(2))
            b = h1_numpy(kk, jobs)
        else:
            m = re.match(r'cheapest_with_voucher\((\d+), (.*)\)$', case['call'])
            n = int(m.group(1))
            links = g['L'] if m.group(2) == 'L' else json.loads(m.group(2))
            b = h2_two_way(n, links)
        rec(b == want, f'{iid}: route B gives {b} = {case["expect"]}')
    rec(slow < 1500, f'{iid}: slowest test {slow:.0f} ms in CPython')
    starter_fails = sum(1 for case in w['tests'] if run_py(w['starter'], case)[0] != eval(case['expect']))
    rec(starter_fails >= 1, f'{iid}: starter fails {starter_fails} of {len(w["tests"])}')
    for name, src in WRONG_PY[iid].items():
        fails = 0
        for case in w['tests']:
            if case.get('setup') and name == 'voucher on every link':
                continue                                   # quadratic search, too slow to run to the end here
            fails += run_py(src, case)[0] != eval(case['expect'])
        rec(fails >= 1, f'{iid}: wrong version "{name}" fails {fails}')

# ---------------------------------------------------------------- H3: the C++ through g++, and NumPy plus brute force
w3 = items['h3-capped-trading']['widget']
rec(w3['language'] == 'cpp' and 3 <= len(w3['tests']) <= 15, f'h3: C++, {len(w3["tests"])} tests')
rec(f'There are {len(w3["tests"])} hidden tests.' in w3['how'], 'h3: how line counts the tests')
CXX = shutil.which('g++') or shutil.which('clang++')


def run_cpp(src, cases):
    body = '\n'.join(f'    std::printf("%lld\\n", (long long)({c["call"]}));' for c in cases)
    prog = src + '\n#include <cstdio>\nint main() {\n' + body + '\n    return 0;\n}\n'
    with tempfile.TemporaryDirectory() as d:
        cpp, exe = os.path.join(d, 'm.cpp'), os.path.join(d, 'm')
        open(cpp, 'w').write(prog)
        subprocess.run([CXX, '-std=c++17', '-O1', '-o', exe, cpp], check=True, capture_output=True)
        t0 = time.perf_counter()
        out = subprocess.run([exe], check=True, capture_output=True, text=True).stdout.split()
        return [int(v) for v in out], time.perf_counter() - t0


A, C = 6364136223846793005, 1442695040888963407


def prices_of(call):
    m = re.match(r'best_cash\(\{(.*)\}, (\d+)\)$', call)
    if m:
        return [int(v) for v in m.group(1).split(',') if v.strip()], int(m.group(2))
    if 'push_back(1000000)' in call:
        return [1, 1000000] * 100000, 1
    seed, n, cap = map(int, re.search(r'p\((\d+)\); unsigned long long s = (\d+)ULL.*best_cash\(p, (\d+)\)', call).group(2, 1, 3))
    xs = list(accumulate(range(n), lambda x, _: (x * A + C) % 2 ** 64, initial=seed))[1:]
    return [1 + (x >> 40) % 1000000 for x in xs], cap


def dp_numpy(prices, cap):
    neg = np.int64(-(1 << 62))
    dp = np.full(cap + 1, neg, dtype=np.int64)
    dp[0] = 0
    for p in prices:
        stay = dp.copy()
        buy = np.full(cap + 1, neg, dtype=np.int64)
        buy[1:] = np.where(dp[:-1] > neg, dp[:-1] - p, neg)
        sell = np.full(cap + 1, neg, dtype=np.int64)
        sell[:-1] = np.where(dp[1:] > neg, dp[1:] + p, neg)
        dp = np.maximum(np.maximum(stay, buy), sell)
    return int(dp[0])


def brute(prices, cap):
    best = 0
    for code in range(3 ** len(prices)):
        held = cash = 0
        ok = True
        for p in prices:
            code, a = divmod(code, 3)
            held += (a == 1) - (a == 2)
            cash += p * ((a == 2) - (a == 1))
            if held < 0 or held > cap:
                ok = False
                break
        if ok and held == 0:
            best = max(best, cash)
    return best


cases3 = w3['examples'] + w3['tests']
got3, secs = run_cpp(w3['solution'], cases3)
for case, got in zip(cases3, got3):
    rec(got == case['expect'], f'h3: g++ solution {case["call"][:50]} = {case["expect"]}', '' if got == case['expect'] else str(got))
    prices, cap = prices_of(case['call'])
    second = brute(prices, cap) if len(prices) <= 10 else dp_numpy(prices, cap)
    rec(second == case['expect'], f'h3: {"brute force" if len(prices) <= 10 else "NumPy DP"} gives {second}')
rec(secs < 2, f'h3: all {len(cases3)} cases run in {secs:.2f} s natively')
rec(cases3[-3]['expect'] == 100000 * 999999, 'h3: alternating 1 and 1,000,000 with cap 1 is 100,000 x 999,999')
rec(all(c['expect'] > 2 ** 31 - 1 for c in w3['tests'][-3:]), 'h3: the last three answers pass 2,147,483,647')
s_out, _ = run_cpp(w3['starter'], w3['tests'])
rec(sum(a != c['expect'] for a, c in zip(s_out, w3['tests'])) >= 1, 'h3: starter fails at least one test')
WRONG_CPP = {
    'int total': w3['solution'].replace('long long', 'int').replace('-(1LL << 62)', '-(1 << 30)').replace('int best_cash', 'long long best_cash'),
    'no cap': w3['solution'].replace('std::vector<long long> dp(cap + 1, NONE), next(cap + 1);', 'cap = (int)prices.size(); std::vector<long long> dp(cap + 1, NONE), next(cap + 1);'),
    'sum of rises': '#include <vector>\nlong long best_cash(const std::vector<int>& prices, int cap) {\n    long long s = 0;\n    for (size_t i = 1; i < prices.size(); ++i) if (cap > 0 && prices[i] > prices[i - 1]) s += prices[i] - prices[i - 1];\n    return s;\n}\n',
    'one share at most': w3['solution'].replace('std::vector<long long> dp(cap + 1, NONE), next(cap + 1);', 'cap = cap > 1 ? 1 : cap; std::vector<long long> dp(cap + 1, NONE), next(cap + 1);'),
}
for name, src in WRONG_CPP.items():
    if name == 'no cap':
        out, _ = run_cpp(src, w3['tests'][:-3])     # quadratic on 200,000 days; the small tests already decide it
        tests = w3['tests'][:-3]
    else:
        out, _ = run_cpp(src, w3['tests'])
        tests = w3['tests']
    fails = sum(a != c['expect'] for a, c in zip(out, tests))
    rec(fails >= 1, f'h3: wrong version "{name}" fails {fails}')

# ---------------------------------------------------------------- every number in every learner-visible string
SKIP = {'starter', 'solution', 'tests', 'examples', 'id', 'tags', 'skills', 'pace', 'difficulty', 'label', 'layout', 'kind', 'language', 'budget'}
ALLOW = {
    'h1-busiest-worker': [2000, 100000, len(items['h1-busiest-worker']['widget']['tests'])],
    'h2-voucher-route': [20000, 100000, len(items['h2-voucher-route']['widget']['tests'])],
    'h3-capped-trading': [200000, 1000000, 100, 2147483647, len(w3['tests'])],
}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, vv in o.items():
            if kk not in SKIP:
                yield from strings(vv, kk)
    elif isinstance(o, list):
        for vv in o:
            yield from strings(vv, k)


for iid, it in items.items():
    bad = []
    for s in strings(it):
        if '—' in s or '–' in s or '!' in re.sub(r'\$[^$]*\$|`[^`]*`', '', s):
            bad.append('dash-or-bang')
        s = re.sub(r'`[^`]*`', ' ', s)
        for m in _NUM.finditer(normalise(s)):
            v = abs(float(m.group(0).rstrip('.')))
            if v == int(v) and v <= 10:
                continue
            if not any(abs(v - a) < 1e-9 for a in ALLOW[iid]):
                bad.append(m.group(0))
    rec(not bad, f'{iid}: every stated number is an input, a count or an answer', f'unmatched {sorted(set(bad))}' if bad else '')

ex.expect('exam', 'models', 90)
ex.expect('exam', 'description', 90)
ex.expect('exam', 'description', 150)
p = doc['parts'][0]
rec(p['minutes'] == 90 and len(p['items']) == 3 and p['pass'] == 0.6, 'paper: 90 minutes, 3 items, pass 0.6 (2 of 3)')
rec(sum(i['pace'] for i in p['items']) <= 90 * 60, 'pace within the paper')
rec(len(doc['models']) <= 200 and 'Reported, as of Nov 2026' in doc['models'], 'models: reported, Nov 2026, under 200 characters')

ex.check_wrongs()
ex.report()
