"""Build app/content/exams/mock-oa-code-hard.json (brief: docs/briefs/mocks.md, section mock-oa-code-hard).

Deterministic: large inputs come from one 64-bit linear congruential generator, written the same way in the hidden
`setup` lines (Python) and `call` lambdas (C++), so CPython, Pyodide and clang see the same numbers. Expected values
are filled by running the reference solutions here (Python in CPython; the C++ reference through a Python port of the
same recurrence) and asserted against a second method on every case. mock-oa-code-hard_check.py is the independent
route over the written file (brute force, NumPy, and the C++ compiled with the local g++). Standard library only.
Run: python3 -I docs/briefs/mocks-scripts/mock-oa-code-hard_build.py
"""
import heapq
import json
import os
from itertools import accumulate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-oa-code-hard.json')
A, C, M = 6364136223846793005, 1442695040888963407, 2 ** 64


def lcg(seed, count):
    """The values after each of `count` steps from `seed` (the seed itself is not returned)."""
    return list(accumulate(range(count), lambda x, _: (x * A + C) % M, initial=seed))[1:]


def py_lcg(seed, count):
    """The same list as Python source for a hidden setup line."""
    return (f'X = list(accumulate(range({count}), lambda x, _: (x * {A} + {C}) % 2**64, initial={seed}))[1:]')


# ---------------------------------------------------------------- H1: jobs on numbered workers (heaps, intervals)
H1_SOL = '''import heapq

def busiest_worker(k, jobs):
    free = list(range(k))
    busy = []
    count = [0] * k
    last = 0
    for arrive, length in sorted(jobs):
        while busy and busy[0][0] <= arrive:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            w, start = heapq.heappop(free), arrive
        else:
            start, w = heapq.heappop(busy)
        end = start + length
        heapq.heappush(busy, (end, w))
        count[w] += 1
        last = max(last, end)
    if not jobs:
        return [0, 0]
    best = min(range(k), key=lambda w: (-count[w], w))
    return [best, last]
'''
H1_START = 'def busiest_worker(k, jobs):\n    return [0, 0]\n'


def h1_scan(k, jobs):
    """Second method: scan every worker for each job (quadratic, exact)."""
    end = [0] * k
    count = [0] * k
    last = 0
    for arrive, length in sorted(jobs):
        free = [w for w in range(k) if end[w] <= arrive]
        if free:
            w, start = free[0], arrive
        else:
            w = min(range(k), key=lambda q: (end[q], q))
            start = end[w]
        end[w] = start + length
        count[w] += 1
        last = max(last, end[w])
    if not jobs:
        return [0, 0]
    return [min(range(k), key=lambda q: (-count[q], q)), last]


h1_ns = {}
exec(H1_SOL, h1_ns)
busiest_worker = h1_ns['busiest_worker']

H1_SMALL = [
    (2, [[0, 10], [1, 2], [2, 5]]),
    (3, []),
    (1, [[5, 2]]),
    (2, [[0, 5], [1, 2], [5, 1]]),
    (2, [[4, 1], [0, 3], [2, 6], [1, 2]]),
    (3, [[0, 4], [1, 4], [2, 4], [3, 1], [5, 1], [6, 1]]),
    (2, [[0, 3], [1, 3], [2, 3], [3, 3], [4, 3]]),
    (4, [[0, 1], [10, 1], [20, 1]]),
    (3, [[0, 100], [1, 1], [2, 1], [3, 1], [50, 100], [60, 5]]),
]
H1_EXAMPLES = [(2, [[0, 10], [1, 2], [2, 5]]), (2, [[0, 5], [1, 2], [5, 1]])]
H1_BIG = [
    ('from itertools import accumulate; ' + py_lcg(7, 100000) + '; J = [[3 * i, 1 + (X[i] >> 40) % 9000] for i in range(100000)][::-1]',
     'list(busiest_worker(2000, J))', lambda: (2000, [[3 * i, 1 + (x >> 40) % 9000] for i, x in enumerate(lcg(7, 100000))][::-1])),
    ('from itertools import accumulate; ' + py_lcg(9, 100000) + '; J = [[3 * i, 1 + (X[i] >> 40) % 18000] for i in range(100000)]',
     'list(busiest_worker(2000, J))', lambda: (2000, [[3 * i, 1 + (x >> 40) % 18000] for i, x in enumerate(lcg(9, 100000))])),
    ('J = [[i, 2] for i in range(100000)]', 'list(busiest_worker(1, J))', lambda: (1, [[i, 2] for i in range(100000)])),
]


def h1_tests():
    tests = []
    for k, jobs in H1_SMALL:
        got = busiest_worker(k, jobs)
        assert got == h1_scan(k, jobs), (k, jobs)
        tests.append({'call': f'list(busiest_worker({k}, {json.dumps(jobs)}))', 'expect': repr(got), 'compare': 'equal'})
    for setup, call, build in H1_BIG:
        k, jobs = build()
        got = busiest_worker(k, jobs)
        if k == 1:
            assert got == [0, 200000]                     # closed form: job i runs from 2i to 2i + 2
        tests.append({'setup': setup, 'call': call, 'expect': repr(got), 'compare': 'equal'})
    return tests


# ---------------------------------------------------------------- H2: cheapest route with one free link (graph with state)
H2_SOL = '''import heapq

def cheapest_with_voucher(n, links):
    adj = [[] for _ in range(n)]
    for u, v, cost in links:
        adj[u].append((v, cost))
    inf = float("inf")
    best = [[inf, inf] for _ in range(n)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        d, u, used = heapq.heappop(heap)
        if d > best[u][used]:
            continue
        if u == n - 1:
            return d
        for v, cost in adj[u]:
            if d + cost < best[v][used]:
                best[v][used] = d + cost
                heapq.heappush(heap, (d + cost, v, used))
            if not used and d < best[v][1]:
                best[v][1] = d
                heapq.heappush(heap, (d, v, 1))
    return -1
'''
H2_START = 'def cheapest_with_voucher(n, links):\n    return -1\n'


def h2_brute(n, links):
    """Second method: plain Bellman-Ford with no voucher and with each link made free in turn."""
    def bf(ls):
        d = [None] * n
        d[0] = 0
        for _ in range(n):
            for u, v, c in ls:
                if d[u] is not None and (d[v] is None or d[u] + c < d[v]):
                    d[v] = d[u] + c
        return d[n - 1]
    outs = [bf(links)] + [bf(links[:i] + [[links[i][0], links[i][1], 0]] + links[i + 1:]) for i in range(len(links))]
    outs = [o for o in outs if o is not None]
    return min(outs) if outs else -1


h2_ns = {}
exec(H2_SOL, h2_ns)
cheapest_with_voucher = h2_ns['cheapest_with_voucher']

H2_SMALL = [
    (4, [[0, 1, 1], [1, 3, 1], [0, 2, 100], [2, 3, 0]]),
    (1, []),
    (3, [[0, 1, 5]]),
    (3, [[1, 0, 1], [2, 1, 1]]),
    (4, [[0, 1, 10], [1, 2, 10], [2, 3, 10]]),
    (2, [[0, 1, 7], [0, 1, 3]]),
    (5, [[0, 1, 4], [1, 4, 4], [0, 2, 1], [2, 3, 1], [3, 4, 9]]),
    (4, [[0, 1, 2], [1, 0, 2], [1, 2, 6], [2, 1, 1], [2, 3, 3], [0, 3, 50]]),
    (6, [[0, 1, 3], [1, 2, 3], [2, 5, 3], [0, 3, 1], [3, 4, 20], [4, 5, 1], [1, 4, 2]]),
]
H2_EXAMPLES = [(4, [[0, 1, 1], [1, 3, 1], [0, 2, 100], [2, 3, 0]]), (3, [[1, 0, 1], [2, 1, 1]])]


def h2_big_links(seed, mod_cost):
    X = lcg(seed, 300000)
    return [[(X[3 * i] >> 40) % 20000, (X[3 * i + 1] >> 40) % 20000, (X[3 * i + 2] >> 40) % mod_cost] for i in range(100000)]


H2_BIG = [
    ('L = [[i, i + 1, 5] for i in range(19999)]', 'cheapest_with_voucher(20000, L)', lambda: [[i, i + 1, 5] for i in range(19999)]),
    ('from itertools import accumulate; ' + py_lcg(11, 300000) + '; L = [[(X[3 * i] >> 40) % 20000, (X[3 * i + 1] >> 40) % 20000, (X[3 * i + 2] >> 40) % 1000] for i in range(100000)]',
     'cheapest_with_voucher(20000, L)', lambda: h2_big_links(11, 1000)),
    ('from itertools import accumulate; ' + py_lcg(13, 300000) + '; L = [[(X[3 * i] >> 40) % 20000, (X[3 * i + 1] >> 40) % 20000, (X[3 * i + 2] >> 40) % 40] for i in range(100000)]',
     'cheapest_with_voucher(20000, L)', lambda: h2_big_links(13, 40)),
]


def h2_tests():
    tests = []
    for n, links in H2_SMALL:
        got = cheapest_with_voucher(n, links)
        assert got == h2_brute(n, links), (n, links, got)
        tests.append({'call': f'cheapest_with_voucher({n}, {json.dumps(links)})', 'expect': repr(got), 'compare': 'equal'})
    for setup, call, build in H2_BIG:
        got = cheapest_with_voucher(20000, build())
        assert got > 0
        if setup.startswith('L = [[i, i + 1, 5]'):
            assert got == 19998 * 5
        tests.append({'setup': setup, 'call': call, 'expect': repr(got), 'compare': 'equal'})
    return tests


# ---------------------------------------------------------------- H3: one share a day with a holding cap (DP with state), C++
H3_SOL = '''#include <vector>
#include <algorithm>

long long best_cash(const std::vector<int>& prices,
                    int cap) {
    const long long NONE = -(1LL << 62);
    std::vector<long long> dp(cap + 1, NONE), next(cap + 1);
    dp[0] = 0;
    for (int p : prices) {
        for (int h = 0; h <= cap; ++h) {
            long long best = dp[h];
            if (h > 0 && dp[h - 1] != NONE) best = std::max(best, dp[h - 1] - p);
            if (h < cap && dp[h + 1] != NONE) best = std::max(best, dp[h + 1] + p);
            next[h] = best;
        }
        dp.swap(next);
    }
    return dp[0];
}
'''
H3_START = '''#include <vector>
#include <algorithm>

long long best_cash(const std::vector<int>& prices,
                    int cap) {
    // your code here
    return 0;
}
'''


def best_cash(prices, cap):
    """Python port of the C++ reference: best cash holding h shares, day by day."""
    none = None
    dp = [0] + [none] * cap
    for p in prices:
        nxt = []
        for h in range(cap + 1):
            best = dp[h]
            if h > 0 and dp[h - 1] is not None:
                best = dp[h - 1] - p if best is None else max(best, dp[h - 1] - p)
            if h < cap and dp[h + 1] is not None:
                best = dp[h + 1] + p if best is None else max(best, dp[h + 1] + p)
            nxt.append(best)
        dp = nxt
    return dp[0]


def best_cash_brute(prices, cap):
    """Second method: every sequence of buy, sell or wait (3 ** n), for small n."""
    best = 0
    def go(t, held, cash):
        nonlocal best
        if t == len(prices):
            if held == 0:
                best = max(best, cash)
            return
        go(t + 1, held, cash)
        if held < cap:
            go(t + 1, held + 1, cash - prices[t])
        if held > 0:
            go(t + 1, held - 1, cash + prices[t])
    go(0, 0, 0)
    return best


H3_SMALL = [
    ([3, 1, 4, 1, 5], 1),
    ([], 3),
    ([5, 4, 3, 2], 2),
    ([1, 2, 3, 4], 2),
    ([1, 2, 3, 4], 1),
    ([7], 1),
    ([2, 9], 0),
    ([1, 1, 10, 10], 2),
    ([4, 1, 3, 2, 8, 1, 6], 3),
    ([6, 1, 2, 9, 3, 3, 10, 1], 2),
]
H3_EXAMPLES = [([3, 1, 4, 1, 5], 1), ([1, 2, 3, 4], 2)]


def cpp_list(xs):
    return '{' + ', '.join(str(v) for v in xs) + '}'


def cpp_lcg_call(seed, n, cap):
    return (f'[&]{{ std::vector<int> p({n}); unsigned long long s = {seed}ULL; for (auto& v : p) '
            f'{{ s = s * {A}ULL + {C}ULL; v = 1 + (int)((s >> 40) % 1000000ULL); }} return best_cash(p, {cap}); }}()')


def lcg_prices(seed, n):
    return [1 + (x >> 40) % 1000000 for x in lcg(seed, n)]


H3_BIG = [
    ('[&]{ std::vector<int> p; for (int i = 0; i < 100000; ++i) { p.push_back(1); p.push_back(1000000); } return best_cash(p, 1); }()',
     lambda: ([1, 1000000] * 100000, 1)),
    (cpp_lcg_call(17, 200000, 50), lambda: (lcg_prices(17, 200000), 50)),
    (cpp_lcg_call(19, 200000, 100), lambda: (lcg_prices(19, 200000), 100)),
]


def h3_tests():
    tests = []
    for prices, cap in H3_SMALL:
        got = best_cash(prices, cap)
        assert got == best_cash_brute(prices, cap), (prices, cap)
        tests.append({'call': f'best_cash({cpp_list(prices)}, {cap})', 'expect': got, 'compare': 'equal'})
    for call, build in H3_BIG:
        prices, cap = build()
        got = best_cash(prices, cap)
        if cap == 1 and prices[:2] == [1, 1000000]:
            assert got == 100000 * 999999                     # closed form: buy at 1, sell at 1,000,000, 100,000 times
        assert 2 ** 31 < got < 2 ** 53
        tests.append({'call': call, 'expect': got, 'compare': 'equal'})
    return tests


# ---------------------------------------------------------------- the exam
t1, t2, t3 = h1_tests(), h2_tests(), h3_tests()
ex1 = [{'call': f'list(busiest_worker({k}, {json.dumps(j)}))', 'expect': repr(busiest_worker(k, j)), 'compare': 'equal'} for k, j in H1_EXAMPLES]
ex2 = [{'call': f'cheapest_with_voucher({n}, {json.dumps(ls)})', 'expect': repr(cheapest_with_voucher(n, ls)), 'compare': 'equal'} for n, ls in H2_EXAMPLES]
ex3 = [{'call': f'best_cash({cpp_list(p)}, {c})', 'expect': best_cash(p, c), 'compare': 'equal'} for p, c in H3_EXAMPLES]
for t in t1 + t2:
    if t.get('setup'):
        t['budget'] = 4000
for t in t3[-3:]:
    t['budget'] = 3000

items = [
    {'id': 'h1-busiest-worker', 'difficulty': 4, 'skills': ['ds-trees', 'ci-patterns'], 'tags': ['job-scheduling', 'heaps'], 'pace': 1500,
     'title': 'Jobs on numbered workers',
     'question': '`k` workers are numbered 0 to `k - 1`. `jobs[i] = [arrive, length]`, and no two jobs arrive at the same time. '
                 'Jobs are handled in order of arrival, though the list may come in any order. A job takes the free worker with '
                 'the lowest number. If none is free, it waits for the worker that frees first (the lower number on a tie). '
                 'It then starts and runs for its full length. A worker that frees at time `t` can take a job that arrives at `t`. '
                 'Write `busiest_worker(k, jobs)`, which returns `[busiest, last_end]`. `busiest` is the worker that ran the '
                 'most jobs, the lowest number on a tie. `last_end` is the time the last job ends. With no jobs it returns '
                 '`[0, 0]`. There may be 2,000 workers and 100,000 jobs.',
     'widget': {'kind': 'code', 'language': 'python', 'starter': H1_START, 'examples': ex1, 'tests': t1,
                'how': f'There are {len(t1)} hidden tests. Each answer must equal the expected value. '
                       'The last three use 100,000 jobs, two of them with 2,000 workers.',
                'solution': H1_SOL},
     'feedback': {'correct': 'All the tests pass, including 100,000 jobs on 2,000 workers.',
                  'generic': 'A hidden test failed. Check a worker that frees as a job arrives, a job that waits, and the large cases.'},
     'explain': {'text': 'Keep two heaps: free workers by number, and busy workers by finish time, then number. '
                         'Before each job, free every finished worker, or else take the earliest finisher. '
                         'Each job then costs $O(\\log k)$, where a scan of all workers costs $O(k)$ and stops on the large tests.'}},
    {'id': 'h2-voucher-route', 'difficulty': 4, 'skills': ['gd-paths', 'ci-timed'], 'tags': ['voucher-route', 'state-graph'], 'pace': 1800,
     'title': 'The cheapest route with one free link',
     'question': 'Sites are numbered 0 to `n - 1`. `links[i] = [u, v, cost]` is a one-way link from site `u` to site `v`, and '
                 '`cost` is a whole number, 0 or more. You hold one voucher, which makes one link of your route free. Write '
                 '`cheapest_with_voucher(n, links)`. It returns the least total cost from site 0 to site `n - 1`, or -1 if '
                 'that site cannot be reached. There may be 20,000 sites and 100,000 links.',
     'widget': {'kind': 'code', 'language': 'python', 'starter': H2_START, 'examples': ex2, 'tests': t2,
                'how': f'There are {len(t2)} hidden tests. Each answer must equal the expected value. '
                       'The last three use 20,000 sites. One small test fails a voucher spent on the cheapest plain route.',
                'solution': H2_SOL},
     'feedback': {'correct': 'All the tests pass, including the 100,000 links.',
                  'generic': 'A hidden test failed. Check a route that is dear before the voucher, one-way links, and a site that cannot be reached.'},
     'explain': {'text': 'Run Dijkstra on pairs (site, voucher used or not), so each site has two best costs. '
                         'A link costs its price, or nothing if the voucher is unused; that step lands in the used copy. '
                         'Spending the voucher on the cheapest plain route can lose to a dearer route made cheap.'}},
    {'id': 'h3-capped-trading', 'difficulty': 5, 'skills': ['gd-dp', 'cp-stl', 'ci-timed'], 'tags': ['inventory-dp', 'cpp'], 'pace': 1800,
     'title': 'One share a day, with a cap',
     'question': '`prices[t]` is the price of one share on day `t`. Each day you may buy one share, sell one share, or do '
                 'nothing. You may never hold more than `cap` shares, or fewer than 0. You start with no shares and must end '
                 'with none. Cash may go below zero along the way. Write `best_cash(prices, cap)` in C++. It returns the most '
                 'cash you can end with. There may be 200,000 days, prices up to 1,000,000 and a `cap` up to 100.',
     'widget': {'kind': 'code', 'language': 'cpp', 'starter': H3_START, 'examples': ex3, 'tests': t3,
                'how': f'There are {len(t3)} hidden tests. Each answer must equal the expected value. '
                       'The last three use 200,000 days, and their answers do not fit in an `int`.',
                'solution': H3_SOL},
     'feedback': {'correct': 'All the tests pass, including 200,000 days with a cap of 100.',
                  'generic': 'A hidden test failed. Check the cap, ending with no shares, and a total that passes 2,147,483,647.'},
     'explain': {'text': 'Keep the best cash for each number of shares held, from 0 to `cap`, and update it once a day. '
                         'Holding $h$ comes from holding $h$, from $h - 1$ and a buy, or from $h + 1$ and a sale. '
                         'That is $O(n \\cdot \\text{cap})$ work, and the totals need a `long long`.'}},
]

exam = {
    'id': 'mock-oa-code-hard',
    'name': 'Harder coding assessment',
    'style': 'developer',
    'models': 'Reported, as of Nov 2026: harder developer coding tests, as at Hudson River Trading and Citadel. Three problems in 90 minutes, one in C++.',
    'description': 'This is a harder coding assessment for developer roles, in a format candidates reported by Nov 2026. '
                   'You have three problems in 90 minutes. '
                   'The first two are in Python and the third is in C++, as some reported tests are C++ only. '
                   'Hidden tests include large inputs, so a slow answer fails them. '
                   'A problem scores only when all its hidden tests pass. '
                   'You pass the paper with two problems of the three. '
                   'Reports differ: three or four problems, in 70 to 150 minutes. '
                   'Read all three statements first, then start with the one you can finish. '
                   'Use no search engine and no notes.',
    'requires': ['coding-int/L4', 'graphs-dp/L4', 'cpp/L4'],
    'skills': {'ds-trees': 'Trees and heaps', 'ci-patterns': 'Further patterns', 'gd-paths': 'Shortest paths',
               'gd-dp': 'Dynamic programming', 'cp-stl': 'The standard library', 'ci-timed': 'Solving under time'},
    'parts': [
        {'kind': 'paper', 'id': 'code', 'name': 'Three problems in ninety minutes', 'minutes': 90,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 0.6, 'items': items},
        {'kind': 'check', 'id': 'read-all', 'name': 'I read all three statements before I wrote any code',
         'detail': 'Tick this only if you chose your order of work before you started.'},
        {'kind': 'check', 'id': 'no-lookup', 'name': 'I used no search engine and no notes',
         'detail': 'Tick this only if you sat the whole paper without either.'},
    ],
}
assert sum(it['pace'] for it in items) == 5100 and len(exam['models']) <= 200

with open(OUT, 'w', encoding='utf8') as f:
    json.dump(exam, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('H1', [t['expect'] for t in t1])
print('H2', [t['expect'] for t in t2])
print('H3', [t['expect'] for t in t3])
print('ALL AGREE')
