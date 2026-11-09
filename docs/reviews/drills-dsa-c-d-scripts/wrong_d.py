# Planted wrong solutions for sub-pack D and the three rewritten B drills.
# Labels: 1 = off by one or boundary, 2 = tie or order slip or a wrong greedy, 3 = the slow method, 4+ = extra.
import json, os, sys
DD = sys.argv[3]


def model(i):
    return json.load(open(os.path.join(DD, i + '.json')))['solution']


def rep(i, *pairs):
    s = model(i)
    for a, b in pairs:
        assert a in s, (i, a)
        s = s.replace(a, b)
    return s


WRONG = {
    'dsa-lift-buttons': [
        ('1 floor 0 allowed', rep('dsa-lift-buttons', ('if 1 <= y <= n', 'if 0 <= y <= n'))),
        ('V greedy up if below, else down (agrees with BFS for every n <= 12, see extra_checks)', 'def solve_lift_buttons(text):\n    n, s, g, u, d = map(int, text.split()); c = 0; seen = set()\n    while s != g:\n        if s in seen: return "-1"\n        seen.add(s)\n        if s < g and s + u <= n and u: s += u\n        elif s - d >= 1 and d: s -= d\n        elif s + u <= n and u: s += u\n        else: return "-1"\n        c += 1\n    return str(c)\n'),
        ('3 relax every floor until stable', 'def solve_lift_buttons(text):\n    n, s, g, u, d = map(int, text.split()); INF = 10**9; dist = [INF] * (n + 2); dist[s] = 0\n    ch = True\n    while ch:\n        ch = False\n        for x in range(1, n + 1):\n            if dist[x] < INF:\n                for y in (x + u, x - d):\n                    if 1 <= y <= n and dist[x] + 1 < dist[y]: dist[y] = dist[x] + 1; ch = True\n    return str(dist[g] if dist[g] < INF else -1)\n'),
    ],
    'dsa-spare-cables': [
        ('1 no cable-count check', rep('dsa-spare-cables', ('if len(cables) < n - 1:\n        return -1', 'pass'))),
        ('2 spare cables counted', rep('dsa-spare-cables', ('return groups - 1', 'return len(cables) - (n - groups)'))),
        ('3 recursive walk', 'import sys\nsys.setrecursionlimit(3000)\ndef spare_cable_moves(n, cables):\n    if len(cables) < n - 1: return -1\n    adj = [[] for _ in range(n)]\n    for a, b in cables: adj[a].append(b); adj[b].append(a)\n    seen = [False] * n\n    def go(x):\n        seen[x] = True\n        for y in adj[x]:\n            if not seen[y]: go(y)\n    c = 0\n    for v in range(n):\n        if not seen[v]: c += 1; go(v)\n    return c - 1\n'),
    ],
    'dsa-climb-limit': [
        ('1 two-way rule (abs)', rep('dsa-climb-limit', ('heights[nr][nc] - h <= climb', 'abs(heights[nr][nc] - h) <= climb'))),
        ('2 rule tested backwards', rep('dsa-climb-limit', ('heights[nr][nc] - h <= climb', 'h - heights[nr][nc] <= climb'))),
        ('3 depth-first, first route found', rep('dsa-climb-limit', ('r, c = queue.popleft()', 'r, c = queue.pop()'))),
    ],
    'dsa-upstream-stations': [
        ('1 downstream search', rep('dsa-upstream-stations', ('back[b].append(a)', 'back[a].append(b)'))),
        ('2 r kept on a loop', 'def upstream_stations(n, pipes, r):\n    back = [[] for _ in range(n)]\n    for a, b in pipes: back[b].append(a)\n    seen = [False] * n; st = [r]; out = set()\n    while st:\n        x = st.pop()\n        for y in back[x]:\n            if not seen[y]: seen[y] = True; out.add(y); st.append(y)\n    return sorted(out)\n'),
        ('3 forward search from each station', 'def upstream_stations(n, pipes, r):\n    adj = [[] for _ in range(n)]\n    for a, b in pipes: adj[a].append(b)\n    out = []\n    for s in range(n):\n        if s == r: continue\n        seen = {s}; st = [s]; hit = False\n        while st and not hit:\n            x = st.pop()\n            for y in adj[x]:\n                if y == r: hit = True; break\n                if y not in seen: seen.add(y); st.append(y)\n        if hit: out.append(s)\n    return out\n'),
    ],
    'dsa-forced-order': [
        ('1 no loop check', rep('dsa-forced-order', ('return order if len(order) == n else None', 'return order'))),
        ('2 only the first pool checked', 'def forced_order(n, deps):\n    after = [[] for _ in range(n)]; need = [0] * n\n    for a, b in deps: after[a].append(b); need[b] += 1\n    ready = [v for v in range(n) if need[v] == 0]\n    if len(ready) != 1: return None\n    order = []\n    while ready:\n        v = ready.pop(); order.append(v)\n        for w in after[v]:\n            need[w] -= 1\n            if need[w] == 0: ready.append(w)\n    return order if len(order) == n else None\n'),
        ('3 rescan all jobs each step', 'def forced_order(n, deps):\n    need = [0] * n; after = [[] for _ in range(n)]\n    for a, b in deps: need[b] += 1; after[a].append(b)\n    done = [False] * n; order = []\n    for _ in range(n):\n        free = [v for v in range(n) if not done[v] and need[v] == 0]\n        if len(free) != 1: return None\n        v = free[0]; done[v] = True; order.append(v)\n        for w in after[v]: need[w] -= 1\n    return order\n'),
        ('4 rule counted in need each time, but stored once in after', 'def forced_order(n, deps):\n    after = [[] for _ in range(n)]; need = [0] * n\n    for a, b in set(deps): after[a].append(b)\n    for a, b in deps: need[b] += 1\n    ready = [v for v in range(n) if need[v] == 0]; order = []\n    while ready:\n        if len(ready) > 1: return None\n        v = ready.pop(); order.append(v)\n        for w in after[v]:\n            need[w] -= 1\n            if need[w] == 0: ready.append(w)\n    return order if len(order) == n else None\n'),
    ],
    'dsa-footpath-slabs': [
        ('1 n = 0 gives 0', rep('dsa-footpath-slabs', ('return cur if n > 0 else 1', 'return cur if n > 0 else 0'))),
        ('2 square forgotten (Fibonacci)', rep('dsa-footpath-slabs', ('(cur + 2 * prev) % MOD', '(cur + prev) % MOD'))),
        ('3 big integers, modulo at the end', 'def footpath_ways(n):\n    a, b = 1, 1\n    for _ in range(n - 1): a, b = b, b + 2 * a\n    return (b if n else 1) % 1_000_000_007\n'),
        ('4 memoised recursion', 'from functools import lru_cache\nimport sys\nsys.setrecursionlimit(5000)\n@lru_cache(None)\ndef footpath_ways(n):\n    if n < 2: return 1\n    return (footpath_ways(n - 1) + 2 * footpath_ways(n - 2)) % 1_000_000_007\n'),
    ],
    'dsa-stamp-gaps': [
        ('1 limit itself never filled', rep('dsa-stamp-gaps', ('for total in range(1, limit + 1):', 'for total in range(1, limit):'))),
        ('2 greedy largest stamp first', 'def unpayable_totals(stamps, limit):\n    st = sorted(set(stamps), reverse=True); bad = 0\n    for t in range(1, limit + 1):\n        r = t\n        for s in st: r %= s\n        bad += r != 0\n    return bad\n'),
        ('3 one stamp value at a time (no mixing)', 'def unpayable_totals(stamps, limit):\n    return sum(1 for t in range(1, limit + 1) if not any(t % s == 0 for s in stamps))\n'),
        ('4 search through combinations', 'def unpayable_totals(stamps, limit):\n    st = sorted(set(stamps))\n    def can(t, i):\n        if t == 0: return True\n        if i == len(st): return False\n        return any(can(t - j * st[i], i + 1) for j in range(t // st[i] + 1))\n    return sum(1 for t in range(1, limit + 1) if not can(t, 0))\n'),
    ],
    'dsa-shift-pay': [
        ('1 states start at 0 (note 1 trap)', rep('dsa-shift-pay', ('rest, one, two = 0, NEG, NEG', 'rest, one, two = 0, 0, 0'))),
        ('2 no two days in a row', 'def solve_shift_pay(text):\n    d = text.split(); n = int(d[0]); a = b = 0\n    for x in map(int, d[1:1 + n]): a, b = max(a, b), a + x\n    return str(max(a, b))\n'),
        ('3 rest the cheapest day of each block of three', 'def solve_shift_pay(text):\n    d = list(map(int, text.split())); n = d[0]; p = d[1:1 + n]; t = 0\n    for i in range(0, n, 3):\n        blk = p[i:i + 3]\n        t += sum(blk) - (min(blk) if len(blk) == 3 else 0)\n    return str(t)\n'),
        ('4 two-in-a-row may work again', rep('dsa-shift-pay', ('rest, one, two = max(rest, one, two), rest + x, one + x', 'rest, one, two = max(rest, one, two), max(rest, two) + x, one + x'))),
    ],
    'dsa-feed-passes': [
        ('1 pass covers one day too many', rep('dsa-feed-passes', ('bisect_left(days, days[i] + length)', 'bisect_left(days, days[i] + length + 1)'))),
        ('2 greedy: 7-day pass when 3 or more days fall in it', 'from bisect import bisect_left\ndef solve_feed_passes(text):\n    d = list(map(int, text.split())); n, p1, p7, p30 = d[:4]; days = d[4:4 + n]; i = c = 0\n    while i < n:\n        j30 = bisect_left(days, days[i] + 30); j7 = bisect_left(days, days[i] + 7)\n        if (j30 - i) * p1 > p30 and p30 <= p7 * ((j30 - i + 6) // 7): c += p30; i = j30\n        elif (j7 - i) * p1 > p7: c += p7; i = j7\n        else: c += p1; i += 1\n    return str(c)\n'),
        ('3 table over every calendar day', 'def solve_feed_passes(text):\n    d = list(map(int, text.split())); n, p1, p7, p30 = d[:4]; days = d[4:4 + n]\n    if not n: return "0"\n    need = set(days); last = days[-1]; best = [0] * (last + 1)\n    for t in range(1, last + 1):\n        if t not in need: best[t] = best[t - 1]\n        else: best[t] = min(best[t - 1] + p1, best[max(0, t - 7)] + p7, best[max(0, t - 30)] + p30)\n    return str(best[last])\n'),
    ],
    'dsa-free-desk-square': [
        ('1 only above and left', rep('dsa-free-desk-square', ('min(above[c], cur[c - 1], above[c - 1])', 'min(above[c], cur[c - 1])'))),
        ('2 first column scores 0', rep('dsa-free-desk-square', ('if c == 0:\n                    cur[c] = 1', 'if c == 0:\n                    cur[c] = 0'))),
        ('3 corner search that tries only sizes above the best so far', 'def largest_free_square(plan):\n    R, C = len(plan), len(plan[0]); best = 0\n    for r in range(R):\n        for c in range(C):\n            k = best + 1\n            while r + k <= R and c + k <= C and all(plan[r + i][c:c + k] == "." * k for i in range(k)):\n                best = k; k += 1\n    return best\n'),
        ('3b every size from 1 at every corner', 'def largest_free_square(plan):\n    R, C = len(plan), len(plan[0]); best = 0\n    for r in range(R):\n        for c in range(C):\n            k = 1\n            while r + k <= R and c + k <= C and all(plan[r + i][c:c + k] == "." * k for i in range(k)):\n                best = max(best, k); k += 1\n    return best\n'),
    ],
    'dsa-kiosk-change': [
        ('1 three fives first (wrong greedy)', 'def first_short_change(notes):\n    f = t = 0\n    for i, x in enumerate(notes):\n        if x == 5: f += 1\n        elif x == 10:\n            if not f: return i\n            f -= 1; t += 1\n        elif f >= 3: f -= 3\n        elif t and f: t -= 1; f -= 1\n        else: return i\n    return -1\n'),
        ('2 no three-fives fallback', rep('dsa-kiosk-change', ('        elif fives >= 3:\n            fives -= 3\n', ''))),
        ('3 recount the till from the start', 'def first_short_change(notes):\n    for k in range(len(notes)):\n        f = t = 0; ok = True\n        for x in notes[:k + 1]:\n            if x == 5: f += 1\n            elif x == 10:\n                if not f: ok = False; break\n                f -= 1; t += 1\n            elif t and f: t -= 1; f -= 1\n            elif f >= 3: f -= 3\n            else: ok = False; break\n        if not ok: return k\n    return -1\n'),
        ('4 a 10 may be paid back with a 10', 'def first_short_change(notes):\n    f = t = 0\n    for i, x in enumerate(notes):\n        if x == 5: f += 1\n        elif x == 10:\n            if f: f -= 1\n            else: return i\n            t += 1\n        elif t >= 1 and f >= 1: t -= 1; f -= 1\n        elif f >= 3: f -= 3\n        elif t >= 2: t -= 2\n        else: return i\n    return -1\n'),
    ],
    'dsa-loop-depots': [
        ('1 no total check', rep('dsa-loop-depots', ('if sum(fuel) < sum(burn):\n        return -1', 'pass'))),
        ('2 restart on an empty tank too', rep('dsa-loop-depots', ('if tank < 0:', 'if tank <= 0 and i + 1 < len(fuel):'))),
        ('3 drive the loop from every depot', 'def loop_start_depot(fuel, burn):\n    n = len(fuel)\n    for s in range(n):\n        t = 0\n        for k in range(n):\n            i = (s + k) % n; t += fuel[i] - burn[i]\n            if t < 0: break\n        else: return s\n    return -1\n'),
    ],
    'dsa-ticker-batches': [
        ('1 end set at the batch start only', 'def ticker_batches(tape):\n    last = {c: i for i, c in enumerate(tape)}; out = []; start = 0; end = -1\n    for i, c in enumerate(tape):\n        if i > end: start = i; end = last[c]\n        if i == end: out.append(i - start + 1)\n    return out\n'),
        ('2 first appearance taken as last', rep('dsa-ticker-batches', ('last = {ch: i for i, ch in enumerate(tape)}', 'last = {}\n    for i, ch in enumerate(tape): last.setdefault(ch, i)'))),
        ('3 compare both sides of every cut', 'def ticker_batches(tape):\n    out = []; start = 0\n    for i in range(1, len(tape) + 1):\n        if not set(tape[start:i]) & set(tape[i:]): out.append(i - start); start = i\n    return out\n'),
    ],
    'dsa-split-prices': [
        ('1 leading zeros allowed', rep('dsa-split-prices', ("        if digits[pos] == '0':\n            return\n", ''))),
        ('2 cap exclusive', rep('dsa-split-prices', ('if price > cap:', 'if price >= cap:'))),
        ('3 no length pruning', rep('dsa-split-prices', ('        if rest < left or rest > left * width:\n            return\n', ''))),
        ('4 output not sorted (longest first)', rep('dsa-split-prices', ('for end in range(pos + 1, min(pos + width, len(digits)) + 1):', 'for end in range(min(pos + width, len(digits)), pos, -1):'), ('if price > cap:\n                break', 'if price > cap:\n                continue'))),
    ],
    'dsa-server-loads': [
        ('1 longest job to least-loaded server', 'def min_peak_load(jobs, k):\n    l = [0] * k\n    for j in sorted(jobs, reverse=True): l[l.index(min(l))] += j\n    return max(l) if jobs else 0\n'),
        ('2 lower bound only', 'def min_peak_load(jobs, k):\n    return max(max(jobs), -(-sum(jobs) // k)) if jobs else 0\n'),
        ('3 every assignment, no pruning', 'import itertools\ndef min_peak_load(jobs, k):\n    best = sum(jobs)\n    for a in itertools.product(range(k), repeat=len(jobs)):\n        l = [0] * k\n        for j, s in zip(jobs, a): l[s] += j\n        best = min(best, max(l))\n    return best\n'),
        ('V valid (not wrong): bound with > prunes less', rep('dsa-server-loads', ('loads[s] + jobs[i] >= best', 'loads[s] + jobs[i] > best'))),
    ],
    'dsa-oncall-rota': [
        ('1 one run per day (trap)', rep('dsa-oncall-rota', ('total += day - left + 1', 'total += 1'))),
        ('2 no left >= guard', rep('dsa-oncall-rota', ('if name in last and last[name] >= left:', 'if name in last:'))),
        ('3 every run with a set', 'def count_clean_runs(rota):\n    t = 0\n    for i in range(len(rota)):\n        s = set()\n        for j in range(i, len(rota)):\n            if rota[j] in s: break\n            s.add(rota[j]); t += 1\n    return t\n'),
    ],
    'dsa-depth-block': [
        ('1 strict on both sides (ties twice)', 'def total_block_floor(d):\n    n = len(d); L = [0] * n; R = [0] * n; st = []\n    for i in range(n):\n        while st and d[st[-1]] > d[i]: st.pop()\n        L[i] = i - (st[-1] if st else -1); st.append(i)\n    st = []\n    for i in range(n - 1, -1, -1):\n        while st and d[st[-1]] > d[i]: st.pop()\n        R[i] = (st[-1] if st else n) - i; st.append(i)\n    return sum(d[i] * L[i] * R[i] for i in range(n))\n'),
        ('2 pop on >= on both sides (ties never)', 'def total_block_floor(d):\n    n = len(d); L = [0] * n; R = [0] * n; st = []\n    for i in range(n):\n        while st and d[st[-1]] >= d[i]: st.pop()\n        L[i] = i - (st[-1] if st else -1); st.append(i)\n    st = []\n    for i in range(n - 1, -1, -1):\n        while st and d[st[-1]] >= d[i]: st.pop()\n        R[i] = (st[-1] if st else n) - i; st.append(i)\n    return sum(d[i] * L[i] * R[i] for i in range(n))\n'),
        ('3 running minimum over every block', 'def total_block_floor(d):\n    t = 0\n    for i in range(len(d)):\n        m = d[i]\n        for j in range(i, len(d)):\n            if d[j] < m: m = d[j]\n            t += m\n    return t\n'),
    ],
    'dsa-range-volumes': [
        ('1 rise[r] - rise[l - 1] (trap)', rep('dsa-range-volumes', ('rise[r - 1] - rise[l - 1]', '(rise[r - 1] - rise[l - 2] if l >= 2 else rise[r - 1])'))),
        ('2 lines split on single spaces', 'def solve_range_volumes(text):\n    L = text.split("\\n"); n, q = map(int, L[0].split(" ")); v = list(map(int, L[1].split(" ")))\n    rise = [0] * n\n    for i in range(1, n): rise[i] = rise[i - 1] + (v[i] > v[i - 1])\n    out = []\n    for k in range(q):\n        l, r = map(int, L[2 + k].split(" ")); out.append(str(rise[r - 1] - rise[l - 1]))\n    return "\\n".join(out)\n'),
        ('3 count each range afresh', 'def solve_range_volumes(text):\n    t = list(map(int, text.split())); n, q = t[0], t[1]; v = t[2:2 + n]; out = []; p = 2 + n\n    for _ in range(q):\n        l, r = t[p], t[p + 1]; p += 2\n        out.append(str(sum(1 for i in range(l, r) if v[i] > v[i - 1])))\n    return "\\n".join(out)\n'),
    ],
}
