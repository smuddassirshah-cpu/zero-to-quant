# Planted wrong solutions for sub-pack C. Labels: 1 = off by one or boundary, 2 = tie or order slip,
# 3 = the slow method the constraints name, 4+ = extra traps from the notes.
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
    'dsa-route-order': [
        ('1 start at legs[0]', 'def route_order(legs):\n    nxt = dict((a, b) for a, b in legs)\n    stop = legs[0][0] if legs else None\n    out = []\n    while stop is not None:\n        out.append(stop); stop = nxt[stop]\n    return out\n'),
        ('2 no default on empty', rep('dsa-route-order', ('if s not in pointed), None)', 'if s not in pointed))')) ),
        ('3 scan list for next stop', 'def route_order(legs):\n    pointed = {b for a, b in legs}\n    stop = next((a for a, b in legs if a not in pointed), None)\n    out = []\n    while stop is not None:\n        out.append(stop)\n        stop = next(b for a, b in legs if a == stop)\n    return out\n'),
    ],
    'dsa-shallowest-leaf': [
        ('1 None scores 0 (trap)', 'def fewest_checks(t):\n    if t is None: return 0\n    return 1 + min(fewest_checks(t[1]), fewest_checks(t[2]))\n'),
        ('2 height not shortest', 'def fewest_checks(t):\n    if t is None: return 0\n    return 1 + max(fewest_checks(t[1]), fewest_checks(t[2]))\n'),
        ('3 child worked out twice', 'def fewest_checks(t):\n    if t is None: return 0\n    _, l, r = t\n    if l is None and r is None: return 1\n    if l is None: return 1 + fewest_checks(r)\n    if r is None: return 1 + fewest_checks(l)\n    return 1 + (fewest_checks(l) if fewest_checks(l) < fewest_checks(r) else fewest_checks(r))\n'),
    ],
    'dsa-shared-tail': [
        ('1 step together, no evening', 'def solve_shared_tail(text):\n    t = text.split(); n, a, b = int(t[0]), int(t[1]), int(t[2]); nx = [int(x) for x in t[3:3+n]]\n    while a != b and a != -1 and b != -1:\n        a, b = nx[a], nx[b]\n    return str(a) if a == b else "-1"\n'),
        ('2 parse with split(" ")', 'def solve_shared_tail(text):\n    L = text.split("\\n"); n, a, b = map(int, L[0].split(" ")); nx = [int(x) for x in L[1].split(" ")]\n    s = set()\n    while a != -1: s.add(a); a = nx[a]\n    while b != -1:\n        if b in s: return str(b)\n        b = nx[b]\n    return "-1"\n'),
        ('3 walk A for every node of B', 'def solve_shared_tail(text):\n    t = text.split(); n, a, b = int(t[0]), int(t[1]), int(t[2]); nx = [int(x) for x in t[3:3+n]]\n    while b != -1:\n        x = a\n        while x != -1:\n            if x == b: return str(b)\n            x = nx[x]\n        b = nx[b]\n    return "-1"\n'),
    ],
    'dsa-common-manager': [
        ('1 checks a only', rep('dsa-common-manager', ('if name == a or name == b:', 'if name == a:'))),
        ('2 BST ordering assumed', 'def shared_manager(chart, a, b):\n    t = chart\n    while t is not None:\n        name, l, r = t\n        try:\n            if a < name and b < name: t = l; continue\n            if a > name and b > name: t = r; continue\n        except TypeError: pass\n        return name\n'),
        ('3 fresh search each level', 'def shared_manager(chart, a, b):\n    def has(t, x):\n        st = [t]\n        while st:\n            u = st.pop()\n            if u is None: continue\n            if u[0] == x: return True\n            st.append(u[1]); st.append(u[2])\n        return False\n    t = chart\n    while True:\n        name, l, r = t\n        if name in (a, b): return name\n        if has(l, a) and has(l, b): t = l\n        elif has(r, a) and has(r, b): t = r\n        else: return name\n'),
    ],
    'dsa-closest-level': [
        ('1 tie goes higher', rep('dsa-closest-level', ('(abs(level - p), level) < (abs(best - p), best)', '(abs(level - p), -level) < (abs(best - p), -best)'))),
        ('2 last level on path', 'def nearest_levels(book, prices):\n    out = []\n    for p in prices:\n        t = book; last = None\n        while t is not None:\n            last = t[0]\n            if p == t[0]: break\n            t = t[1] if p < t[0] else t[2]\n        out.append(last)\n    return out\n'),
        ('3 scan every level', 'def nearest_levels(book, prices):\n    vals = []; st = [book]\n    while st:\n        u = st.pop()\n        if u is None: continue\n        vals.append(u[0]); st.append(u[1]); st.append(u[2])\n    return [min(vals, key=lambda v: (abs(v - p), v)) for p in prices]\n'),
    ],
    'dsa-swapped-levels': [
        ('1 first drop only (neighbours)', rep('dsa-swapped-levels', ('return [seq[drops[-1]], seq[drops[0] - 1]]', 'return [seq[drops[0]], seq[drops[0] - 1]]'))),
        ('2 parent-child check only', 'def swapped_levels(book):\n    bad = []\n    def go(t):\n        if t is None: return\n        p, l, r = t\n        if l is not None and l[0] > p: bad.extend([l[0], p])\n        if r is not None and r[0] < p: bad.extend([r[0], p])\n        go(l); go(r)\n    go(book)\n    return [min(bad), max(bad)] if bad else []\n'),
        ('3 try every pair', 'def swapped_levels(book):\n    seq = []\n    def rd(t):\n        if t is None: return\n        rd(t[1]); seq.append(t[0]); rd(t[2])\n    rd(book)\n    if all(seq[i] < seq[i+1] for i in range(len(seq)-1)): return []\n    n = len(seq)\n    for i in range(n):\n        for j in range(i + 1, n):\n            s = seq[:]; s[i], s[j] = s[j], s[i]\n            if all(s[k] < s[k+1] for k in range(n-1)): return [min(seq[i], seq[j]), max(seq[i], seq[j])]\n    return []\n'),
        ('4 in-order by list concatenation O(n h)', 'def swapped_levels(book):\n    def rd(t):\n        return [] if t is None else rd(t[1]) + [t[0]] + rd(t[2])\n    seq = rd(book)\n    d = [i for i in range(1, len(seq)) if seq[i] < seq[i-1]]\n    return [seq[d[-1]], seq[d[0]-1]] if d else []\n'),
    ],
    'dsa-nearest-strikes': [
        ('1 distance only (stable)', 'def nearest_strikes(strikes, spot, k):\n    return sorted(strikes, key=lambda s: abs(s - spot))[:k]\n'),
        ('2 tie to higher strike', 'def nearest_strikes(strikes, spot, k):\n    return sorted(strikes, key=lambda s: (abs(s - spot), -s))[:k]\n'),
        ('3 pick nearest k times', 'def nearest_strikes(strikes, spot, k):\n    left = list(strikes); out = []\n    for _ in range(k):\n        b = min(left, key=lambda s: (abs(s - spot), s)); out.append(b); left.remove(b)\n    return out\n'),
    ],
    'dsa-short-codes': [
        ('1 sort, lcp without +1', 'def short_codes(names):\n    o = sorted(names); need = {}\n    def lcp(a, b):\n        i = 0\n        while i < min(len(a), len(b)) and a[i] == b[i]: i += 1\n        return i\n    for j, w in enumerate(o):\n        m = 0\n        if j: m = max(m, lcp(w, o[j-1]))\n        if j + 1 < len(o): m = max(m, lcp(w, o[j+1]))\n        need[w] = w[:max(m, 1)]\n    return [need[w] for w in names]\n'),
        ('2 no whole-name fallback', rep('dsa-short-codes', ('node, code = root, name', "node, code = root, ''"))),
        ('3 compare every pair', 'def short_codes(names):\n    out = []\n    for w in names:\n        m = 0\n        for x in names:\n            if x is w: continue\n            i = 0\n            while i < min(len(w), len(x)) and w[i] == x[i]: i += 1\n            m = max(m, i)\n        out.append(w[:m + 1])\n    return out\n'),
    ],
    'dsa-print-queue': [
        ('1 arrival at free moment not waiting', rep('dsa-print-queue', ('while i < n and jobs[i][0] <= clock:', 'while i < n and (jobs[i][0] < clock or not waiting and jobs[i][0] <= clock):'))),
        ('2 tie by id, not arrival', rep('dsa-print-queue', ('heapq.heappush(waiting, (pages, arrival, jid))', 'heapq.heappush(waiting, (pages, jid, arrival))'), ('pages, arrival, jid = heapq.heappop(waiting)', 'pages, jid, arrival = heapq.heappop(waiting)'))),
        ('3 scan waiting list', rep('dsa-print-queue', ('heapq.heappush(waiting, (pages, arrival, jid))', 'waiting.append((pages, arrival, jid))'), ('pages, arrival, jid = heapq.heappop(waiting)', 'm = min(waiting); waiting.remove(m); pages, arrival, jid = m'))),
        ('4 push all at start (trap)', 'import heapq\ndef solve_print_queue(text):\n    t = list(map(int, text.split())); n = t[0]\n    h = [(t[3+3*i], t[2+3*i], t[1+3*i]) for i in range(n)]\n    heapq.heapify(h)\n    return " ".join(str(heapq.heappop(h)[2]) for _ in range(n))\n'),
    ],
    'dsa-window-every-venue': [
        ('1 tie to larger lo', rep('dsa-window-every-venue', ('high - low < best[1] - best[0]', 'high - low <= best[1] - best[0]'))),
        ('2 high never raised', rep('dsa-window-every-venue', ('high = max(high, after)', 'pass'))),
        ('V valid variant (not wrong): best kept only at the first visit of each start', rep('dsa-window-every-venue', ('if best is None or high - low < best[1] - best[0]:', 'if best is None or (high - low < best[1] - best[0] and low != best[0]):'))),
        ('3 every start, bisect each list', 'from bisect import bisect_left\ndef tightest_window(feeds):\n    best = None\n    for lo in sorted(set(x for f in feeds for x in f)):\n        hi = lo\n        for f in feeds:\n            j = bisect_left(f, lo)\n            if j == len(f): hi = None; break\n            hi = max(hi, f[j])\n        if hi is None: break\n        if best is None or hi - lo < best[1] - best[0]: best = [lo, hi]\n    return best\n'),
    ],
    'dsa-total-booked': [
        ('1 inclusive end', rep('dsa-total-booked', ('total += cur_end - cur_start\n        cur_start', 'total += cur_end - cur_start + 1\n        cur_start'), ('    if cur_end is not None:\n        total += cur_end - cur_start\n    return', '    if cur_end is not None:\n        total += cur_end - cur_start + 1\n    return'))),
        ('2 sum of lengths (trap)', 'def booked_minutes(b):\n    return sum(e - s for s, e in b)\n'),
        ('3 mark each minute', 'def booked_minutes(b):\n    m = set()\n    for s, e in b: m.update(range(s, e))\n    return len(m)\n'),
        ('4 unsorted merge', rep('dsa-total-booked', ('in sorted(bookings):', 'in bookings:'))),
    ],
    'dsa-double-booked': [
        ('1 <= (trap)', rep('dsa-double-booked', ('if start < end:', 'if start <= end:'))),
        ('2 unsorted neighbours', rep('dsa-double-booked', ('ordered = sorted(slots)', 'ordered = list(slots)'))),
        ('3 every pair', 'def any_clash(s):\n    return any(s[i][0] < s[j][1] and s[j][0] < s[i][1] for i in range(len(s)) for j in range(i + 1, len(s)))\n'),
        ('V valid mirror (not wrong): sort by end, compare neighbours', rep('dsa-double-booked', ('ordered = sorted(slots)', 'ordered = sorted(slots, key=lambda x: x[1])'))),
    ],
    'dsa-peak-calls': [
        ('1 starts before ends', rep('dsa-peak-calls', ('events.sort()', 'events.sort(key=lambda e: (e[0], -e[1]))'))),
        ('2 latest second at the peak', rep('dsa-peak-calls', ('if live > peak:', 'if live >= peak and step == 1:'))),
        ('3 recount at every start', 'def solve_peak_calls(text):\n    t = list(map(int, text.split())); n = t[0]\n    c = [(t[1+2*i], t[2+2*i]) for i in range(n)]\n    best = (0, 0)\n    for s, _ in c:\n        k = sum(1 for a, b in c if a <= s < b)\n        if k > best[0] or (k == best[0] and s < best[1]): best = (k, s)\n    return "%d %d" % best\n'),
    ],
    'dsa-cover-opening': [
        ('1 strict start < reach', rep('dsa-cover-opening', ('ordered[i][0] <= reach', 'ordered[i][0] < reach or (reach == 0 and ordered[i][0] <= 0)'))),
        ('2 longest shift greedy', 'def fewest_shifts(shifts, close):\n    reach = cnt = 0\n    while reach < close:\n        c = [s for s in shifts if s[0] <= reach < s[1]]\n        if not c: return -1\n        b = max(c, key=lambda s: s[1] - s[0]); reach = b[1]; cnt += 1\n    return cnt\n'),
        ('3 every shift that could follow', 'def fewest_shifts(shifts, close):\n    s = sorted(shifts, key=lambda x: x[1]); INF = float("inf"); best = [INF] * len(s)\n    for i, (a, b) in enumerate(s):\n        if a <= 0: best[i] = 1\n        for j in range(i):\n            if s[j][1] >= a and s[j][1] < b and best[j] + 1 < best[i]: best[i] = best[j] + 1\n    r = min([best[i] for i in range(len(s)) if s[i][1] >= close] or [INF])\n    return -1 if r == INF else r\n'),
    ],
    'dsa-shortest-cover': [
        ('1 end covered', rep('dsa-shortest-cover', ('while heap and heap[0][1] <= t:', 'while heap and heap[0][1] < t:'))),
        ('2 input order sweep', 'import heapq\ndef shortest_windows(windows, parcels):\n    o = sorted(windows); h = []; i = 0; out = []\n    for t in parcels:\n        while i < len(o) and o[i][0] <= t:\n            heapq.heappush(h, (o[i][1] - o[i][0], o[i][1])); i += 1\n        while h and h[0][1] <= t: heapq.heappop(h)\n        out.append(h[0][0] if h else -1)\n    return out\n'),
        ('3 every window for every parcel', 'def shortest_windows(windows, parcels):\n    return [min([e - s for s, e in windows if s <= t < e] or [-1]) for t in parcels]\n'),
    ],
}
