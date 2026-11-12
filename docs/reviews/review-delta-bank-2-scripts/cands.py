"""Candidate-wrong solutions for the 13 code tasks whose hidden tests changed (4 of them re-stated), and for binom_tail
(prose changed). Each entry: (name, what is wrong or risky, source). A name starting "alt:" is another right solution
and must give right answers. Written from the statements, before the hidden tests were used to tune anything."""
C = {}

C['edge-case-list-second-largest'] = [
 ('no-dedupe', 'sorted(xs)[-1] - sorted(xs)[-2]', 'def runner_up_gap(xs):\n    if len(xs) < 2: return None\n    s = sorted(xs)\n    return s[-1] - s[-2]\n'),
 ('zero-not-none', 'returns 0 when there is no second value', 'def runner_up_gap(xs):\n    d = sorted(set(xs))\n    return d[-1] - d[-2] if len(d) > 1 else 0\n'),
 ('smallest-gap', 'gap between the two smallest different values', 'def runner_up_gap(xs):\n    d = sorted(set(xs))\n    return d[1] - d[0] if len(d) > 1 else None\n'),
 ('range', 'largest less smallest', 'def runner_up_gap(xs):\n    if len(set(xs)) < 2: return None\n    return max(xs) - min(xs)\n'),
 ('remove-once', 'removes one copy of the largest', 'def runner_up_gap(xs):\n    if len(set(xs)) < 2: return None\n    ys = list(xs); m = max(ys); ys.remove(m)\n    return m - max(ys)\n'),
 ('one-pass-no-neq', 'one pass that lets a repeat of the top value be second', 'def runner_up_gap(xs):\n    a = b = None\n    for x in xs:\n        if a is None or x > a: a, b = x, a\n        elif b is None or x > b: b = x\n    return None if b is None else a - b\n'),
 ('zero-start', 'one pass with the top two started at 0', 'def runner_up_gap(xs):\n    a = b = 0\n    for x in xs:\n        if x > a: a, b = x, a\n        elif a > x > b: b = x\n    return a - b if len(set(xs)) > 1 else None\n'),
 ('len-check', 'tests len(xs) < 2, not the number of different values', 'def runner_up_gap(xs):\n    if len(xs) < 2: return None\n    d = sorted(set(xs))\n    return d[-1] - d[-2]\n'),
 ('negative-gap', 'next value less the largest', 'def runner_up_gap(xs):\n    d = sorted(set(xs))\n    return d[-2] - d[-1] if len(d) > 1 else None\n'),
 ('quadratic', 'max(xs) recomputed for every element', 'def runner_up_gap(xs):\n    rest = [x for x in xs if x != max(xs)]\n    return max(xs) - max(rest) if rest else None\n'),
 ('abs-values', 'compares sizes, so negatives go wrong', 'def runner_up_gap(xs):\n    d = sorted(set(abs(x) for x in xs))\n    return d[-1] - d[-2] if len(d) > 1 else None\n'),
 ('alt:two-max', 'max, then max of the values below it', 'def runner_up_gap(xs):\n    if not xs: return None\n    m = max(xs)\n    rest = [x for x in xs if x < m]\n    return m - max(rest) if rest else None\n'),
]

C['ds-pointers-merge-ticks'] = [
 ('sorted-concat', 'sorted(a + b): both ticks kept', 'def merge_ticks(a, b):\n    return sorted(a + b)\n'),
 ('keep-a', 'at a shared time keeps the first feed', 'def merge_ticks(a, b):\n    d = dict(b); d.update(dict(a))\n    return sorted(d.items())\n'),
 ('keep-b', 'at a shared time keeps the second feed', 'def merge_ticks(a, b):\n    d = dict(a); d.update(dict(b))\n    return sorted(d.items())\n'),
 ('sum-not-mean', 'adds the two prices', 'def merge_ticks(a, b):\n    d = dict(a)\n    for t, p in b: d[t] = d.get(t, 0) + p\n    return sorted(d.items())\n'),
 ('floor-mean', '// 2', 'def merge_ticks(a, b):\n    d = dict(a)\n    for t, p in b: d[t] = (d[t] + p) // 2 if t in d else p\n    return sorted(d.items())\n'),
 ('no-tail', 'two pointers without the rest of the longer list', 'def merge_ticks(a, b):\n    out, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i][0] == b[j][0]: out.append((a[i][0], (a[i][1] + b[j][1]) / 2)); i += 1; j += 1\n        elif a[i][0] < b[j][0]: out.append(a[i]); i += 1\n        else: out.append(b[j]); j += 1\n    return out\n'),
 ('pop0-in-place', 'classic merge with pop(0) on the arguments', 'def merge_ticks(a, b):\n    out = []\n    while a and b:\n        if a[0][0] == b[0][0]: t, p = a.pop(0); q = b.pop(0)[1]; out.append((t, (p + q) / 2))\n        elif a[0][0] < b[0][0]: out.append(a.pop(0))\n        else: out.append(b.pop(0))\n    return out + a + b\n'),
 ('extend-a', 'a.extend(b) then combine: a is changed', 'def merge_ticks(a, b):\n    a.extend(b); a.sort()\n    out = []\n    for t, p in a:\n        if out and out[-1][0] == t: out[-1] = (t, (out[-1][1] + p) / 2)\n        else: out.append((t, p))\n    return out\n'),
 ('mutate-on-shared', 'writes the mean back into a at each shared time (a changes only when the feeds share a time)', 'def merge_ticks(a, b):\n    db = dict(b)\n    for i, (t, p) in enumerate(a):\n        if t in db: a[i] = (t, (p + db[t]) / 2)\n    seen = {t for t, _ in a}\n    return sorted(a + [x for x in b if x[0] not in seen])\n'),
 ('delete-from-b', 'deletes each shared tick from b after averaging it into the result', 'def merge_ticks(a, b):\n    out = []\n    tb = {t: k for k, (t, _) in enumerate(b)}\n    drop = []\n    for t, p in a:\n        if t in tb: out.append((t, (p + b[tb[t]][1]) / 2)); drop.append(tb[t])\n        else: out.append((t, p))\n    for k in reversed(drop): del b[k]\n    return sorted(out + b)\n'),
 ('first-shared-only', 'combines only the first shared time', 'def merge_ticks(a, b):\n    out = sorted(a + b); done = False; res = []\n    for t, p in out:\n        if res and res[-1][0] == t and not done: res[-1] = (t, (res[-1][1] + p) / 2); done = True\n        else: res.append((t, p))\n    return res\n'),
 ('weighted-to-a', 'mean with the wrong weights', 'def merge_ticks(a, b):\n    d = dict(a)\n    for t, p in b: d[t] = (2 * d[t] + p) / 3 if t in d else p\n    return sorted(d.items())\n'),
 ('alt:dict', 'dict of times, right', 'def merge_ticks(a, b):\n    d = dict(a)\n    for t, p in b: d[t] = (d[t] + p) / 2 if t in d else p\n    return sorted(d.items())\n'),
 ('alt:pop0-on-copies', 'copies both lists, then the classic pop(0) merge: right, and the statement gives no size', 'def merge_ticks(a, b):\n    a, b = list(a), list(b)\n    out = []\n    while a and b:\n        if a[0][0] == b[0][0]: t, p = a.pop(0); q = b.pop(0)[1]; out.append((t, (p + q) / 2))\n        elif a[0][0] < b[0][0]: out.append(a.pop(0))\n        else: out.append(b.pop(0))\n    return out + a + b\n'),
 ('alt:scan-b-for-each', 'for each tick of a, looks for its time in a list of b times (quadratic): right, and the statement gives no size', 'def merge_ticks(a, b):\n    tb = [t for t, _ in b]\n    out = []\n    for t, p in a:\n        if t in tb: out.append((t, (p + b[tb.index(t)][1]) / 2))\n        else: out.append((t, p))\n    ta = [t for t, _ in a]\n    out += [x for x in b if x[0] not in ta]\n    return sorted(out)\n'),
]

C['pf-collections-top-symbols'] = [
 ('signed-sum', 'nets sales against purchases', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + q\n    return sorted(t, key=lambda s: -t[s])[:k]\n'),
 ('abs-of-net', 'size of the net position', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + q\n    return sorted(t, key=lambda s: -abs(t[s]))[:k]\n'),
 ('trade-count', 'number of trades', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + 1\n    return sorted(t, key=lambda s: -t[s])[:k]\n'),
 ('ties-alphabetical', 'equal totals by name', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return sorted(t, key=lambda s: (-t[s], s))[:k]\n'),
 ('ties-reversed', 'ascending sort then reversed, so equal totals come last-first', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return sorted(t, key=lambda s: t[s])[::-1][:k]\n'),
 ('buys-only', 'ignores sales', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + max(q, 0)\n    return sorted(t, key=lambda s: -t[s])[:k]\n'),
 ('largest-single', 'largest single trade', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = max(t.get(s, 0), abs(q))\n    return sorted(t, key=lambda s: -t[s])[:k]\n'),
 ('ties-last-trade', 'equal totals by the last trade, not the first (the key is re-inserted)', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.pop(s, 0) + abs(q)\n    return sorted(t, key=lambda s: -t[s])[:k]\n'),
 ('scan-per-symbol', 'sums every trade again for each symbol', 'def busiest_symbols(trades, k):\n    names = []\n    for s, _ in trades:\n        if s not in names: names.append(s)\n    tot = {s: sum(abs(q) for n, q in trades if n == s) for s in names}\n    return sorted(names, key=lambda s: -tot[s])[:k]\n'),
 ('k-minus-one', 'slice off by one', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return sorted(t, key=lambda s: -t[s])[:max(k - 1, 0)] if k < len(t) else list(sorted(t, key=lambda s: -t[s]))\n'),
 ('names-sorted-first', 'names taken from a sorted set, so ties come in name order reversed', 'def busiest_symbols(trades, k):\n    t = {}\n    for s in sorted(set(s for s, _ in trades), reverse=True): t[s] = 0\n    for s, q in trades: t[s] += abs(q)\n    return sorted(t, key=lambda s: -t[s])[:k]\n'),
 ('alt:counter', 'Counter.most_common', 'from collections import Counter\ndef busiest_symbols(trades, k):\n    c = Counter()\n    for s, q in trades: c[s] += abs(q)\n    return [s for s, _ in c.most_common()][:k]\n'),
 ('alt:reverse-true', 'sorted(reverse=True), which is stable', 'def busiest_symbols(trades, k):\n    t = {}\n    for s, q in trades: t[s] = t.get(s, 0) + abs(q)\n    return sorted(t, key=t.get, reverse=True)[:k]\n'),
 ('alt:first-seen-list', 'keeps first-seen order in a list with `in` (right; 100,000 trades are stated, the number of symbols is not)', 'def busiest_symbols(trades, k):\n    names, t = [], {}\n    for s, q in trades:\n        if s not in names: names.append(s)\n        t[s] = t.get(s, 0) + abs(q)\n    return sorted(names, key=lambda s: -t[s])[:k]\n'),
]

C['ds-hashing-price-mode'] = [
 ('single-max', 'one of the tied prices', 'def modal_prices(prices):\n    if not prices: return []\n    c = {}\n    for p in prices: c[p] = c.get(p, 0) + 1\n    return [max(c, key=c.get)]\n'),
 ('ascending', 'lowest first', 'def modal_prices(prices):\n    c = {}\n    for p in prices: c[p] = c.get(p, 0) + 1\n    top = max(c.values(), default=0)\n    return sorted(p for p in c if c[p] == top)\n'),
 ('first-seen', 'order of first appearance (statistics.multimode)', 'from statistics import multimode\ndef modal_prices(prices):\n    return multimode(prices)\n'),
 ('no-empty-guard', 'max of nothing', 'def modal_prices(prices):\n    c = {}\n    for p in prices: c[p] = c.get(p, 0) + 1\n    top = max(c.values())\n    return sorted((p for p in c if c[p] == top), reverse=True)\n'),
 ('with-repeats', 'keeps each modal price once per occurrence', 'def modal_prices(prices):\n    if not prices: return []\n    top = max(prices.count(p) for p in set(prices))\n    return sorted((p for p in prices if prices.count(p) == top), reverse=True)\n'),
 ('at-least-two', 'every price seen more than once', 'def modal_prices(prices):\n    c = {}\n    for p in prices: c[p] = c.get(p, 0) + 1\n    r = sorted((p for p in c if c[p] > 1), reverse=True)\n    return r if r else sorted(c, reverse=True)\n'),
 ('string-sort', 'sorts the prices as text', 'def modal_prices(prices):\n    c = {}\n    for p in prices: c[p] = c.get(p, 0) + 1\n    top = max(c.values(), default=0)\n    return [int(s) for s in sorted((str(p) for p in c if c[p] == top), reverse=True)]\n'),
 ('by-size', 'highest first by size, ignoring sign', 'def modal_prices(prices):\n    c = {}\n    for p in prices: c[p] = c.get(p, 0) + 1\n    top = max(c.values(), default=0)\n    return sorted((p for p in c if c[p] == top), key=abs, reverse=True)\n'),
 ('most-common-order', 'Counter.most_common order among ties', 'from collections import Counter\ndef modal_prices(prices):\n    c = Counter(prices).most_common()\n    return [p for p, n in c if n == c[0][1]]\n'),
 ('top-two', 'the two most frequent prices', 'from collections import Counter\ndef modal_prices(prices):\n    return sorted((p for p, _ in Counter(prices).most_common(2)), reverse=True)\n'),
 ('alt:count-quadratic', 'prices.count for each different price', 'def modal_prices(prices):\n    if not prices: return []\n    s = set(prices)\n    n = {p: prices.count(p) for p in s}\n    top = max(n.values())\n    return sorted((p for p in s if n[p] == top), reverse=True)\n'),
]

C['ds-arrays-sign-changes'] = [
 ('adjacent-only', 'compares neighbours, zeros included', 'def sign_changes(pnl):\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if a * b < 0)\n'),
 ('zero-is-gain', 'a flat day counted as a gain', 'def sign_changes(pnl):\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if (a >= 0) != (b >= 0))\n'),
 ('zero-is-loss', 'a flat day counted as a loss', 'def sign_changes(pnl):\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if (a > 0) != (b > 0))\n'),
 ('zero-is-third-sign', 'sign in -1, 0, 1 and any change counts', 'def sign_changes(pnl):\n    s = [(x > 0) - (x < 0) for x in pnl]\n    return sum(1 for a, b in zip(s, s[1:]) if a != b)\n'),
 ('reset-on-zero', 'a flat day forgets the last sign', 'def sign_changes(pnl):\n    n, last = 0, 0\n    for x in pnl:\n        if x and last and (x > 0) != (last > 0): n += 1\n        last = x\n    return n\n'),
 ('first-counts', 'the first non-zero day counts as a flip', 'def sign_changes(pnl):\n    n, last = 0, 0\n    for x in pnl:\n        if x == 0: continue\n        s = 1 if x > 0 else -1\n        if s != last: n += 1\n        last = s\n    return n\n'),
 ('recursive', 'recursion over the list', 'def sign_changes(pnl):\n    nz = [x for x in pnl if x]\n    def go(i):\n        if i >= len(nz) - 1: return 0\n        return (1 if nz[i] * nz[i + 1] < 0 else 0) + go(i + 1)\n    return go(0)\n'),
 ('remove-zeros-loop', 'while 0 in pnl: pnl.remove(0)', 'def sign_changes(pnl):\n    pnl = list(pnl)\n    while 0 in pnl: pnl.remove(0)\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if a * b < 0)\n'),
 ('ends-stripped-only', 'strips flat days from the ends only', 'def sign_changes(pnl):\n    while pnl and pnl[0] == 0: pnl = pnl[1:]\n    while pnl and pnl[-1] == 0: pnl = pnl[:-1]\n    return sum(1 for a, b in zip(pnl, pnl[1:]) if (a > 0) != (b > 0))\n'),
 ('one-zero-skipped', 'looks one day past a flat day, no further', 'def sign_changes(pnl):\n    n = 0\n    for i in range(len(pnl) - 1):\n        a, b = pnl[i], pnl[i + 1]\n        if b == 0 and i + 2 < len(pnl): b = pnl[i + 2]\n        if a * b < 0: n += 1\n    return n\n'),
 ('alt:filter', 'filter, then neighbours', 'def sign_changes(pnl):\n    nz = [x for x in pnl if x]\n    return sum(1 for a, b in zip(nz, nz[1:]) if (a > 0) != (b > 0))\n'),
]

C['pf-idioms-count-above-mean'] = [
 ('at-least', '>= the mean', 'def above_mean(xs):\n    if not xs: return 0\n    m = sum(xs) / len(xs)\n    return sum(1 for x in xs if x >= m)\n'),
 ('no-guard', 'divides by zero on the empty list', 'def above_mean(xs):\n    m = sum(xs) / len(xs)\n    return sum(1 for x in xs if x > m)\n'),
 ('int-mean', 'int(sum / len): cut towards zero', 'def above_mean(xs):\n    if not xs: return 0\n    m = int(sum(xs) / len(xs))\n    return sum(1 for x in xs if x > m)\n'),
 ('rounded-mean', 'round(mean)', 'def above_mean(xs):\n    if not xs: return 0\n    m = round(sum(xs) / len(xs))\n    return sum(1 for x in xs if x > m)\n'),
 ('median', 'median in place of mean', 'def above_mean(xs):\n    if not xs: return 0\n    s = sorted(xs); n = len(s)\n    m = (s[n // 2] + s[(n - 1) // 2]) / 2\n    return sum(1 for x in xs if x > m)\n'),
 ('distinct', 'counts different values', 'def above_mean(xs):\n    if not xs: return 0\n    m = sum(xs) / len(xs)\n    return len({x for x in xs if x > m})\n'),
 ('mean-each-time', 'recomputes the mean for every value', 'def above_mean(xs):\n    return len([x for x in xs if x > sum(xs) / len(xs)])\n'),
 ('ceil-mean', 'mean rounded up', 'import math\ndef above_mean(xs):\n    if not xs: return 0\n    m = math.ceil(sum(xs) / len(xs))\n    return sum(1 for x in xs if x > m)\n'),
 ('midrange', 'half of max plus min', 'def above_mean(xs):\n    if not xs: return 0\n    m = (max(xs) + min(xs)) / 2\n    return sum(1 for x in xs if x > m)\n'),
 ('below', 'counts values below the mean', 'def above_mean(xs):\n    if not xs: return 0\n    m = sum(xs) / len(xs)\n    return sum(1 for x in xs if x < m)\n'),
 ('abs-mean', 'mean of the sizes', 'def above_mean(xs):\n    if not xs: return 0\n    m = sum(abs(x) for x in xs) / len(xs)\n    return sum(1 for x in xs if x > m)\n'),
 ('alt:floor-mean', 'sum // len: right for whole numbers', 'def above_mean(xs):\n    if not xs: return 0\n    m = sum(xs) // len(xs)\n    return sum(1 for x in xs if x > m)\n'),
]

C['ds-arrays-local-peaks'] = [
 ('at-least', '>= both neighbours', 'def local_peaks(xs):\n    return [i for i in range(1, len(xs) - 1) if xs[i - 1] <= xs[i] >= xs[i + 1]]\n'),
 ('ends-count', 'ends compared with their one neighbour', 'def local_peaks(xs):\n    n = len(xs); out = []\n    for i in range(n):\n        l = xs[i - 1] if i > 0 else float("-inf")\n        r = xs[i + 1] if i < n - 1 else float("-inf")\n        if n > 1 and l < xs[i] > r: out.append(i)\n    return out\n'),
 ('wraps', 'index -1 wraps to the last value', 'def local_peaks(xs):\n    return [i for i in range(len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]\n'),
 ('values', 'returns the values', 'def local_peaks(xs):\n    return [xs[i] for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]\n'),
 ('one-based', 'positions from 1', 'def local_peaks(xs):\n    return [i + 1 for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]\n'),
 ('left-only', 'greater than the left neighbour only', 'def local_peaks(xs):\n    return [i for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i]]\n'),
 ('max-of-three', 'equals the max of its window', 'def local_peaks(xs):\n    return [i for i in range(1, len(xs) - 1) if xs[i] == max(xs[i - 1:i + 2])]\n'),
 ('index-of', 'xs.index of each peak value', 'def local_peaks(xs):\n    return [xs.index(xs[i]) for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]\n'),
 ('last-included', 'range runs to the last index, guarded by try', 'def local_peaks(xs):\n    out = []\n    for i in range(1, len(xs)):\n        try:\n            if xs[i - 1] < xs[i] > xs[i + 1]: out.append(i)\n        except IndexError:\n            if xs[i - 1] < xs[i]: out.append(i)\n    return out\n'),
 ('skip-after-peak', 'jumps two after a peak, and so can pass one', 'def local_peaks(xs):\n    out, i = [], 1\n    while i < len(xs) - 1:\n        if xs[i - 1] < xs[i] and xs[i] >= xs[i + 1]: out.append(i); i += 2\n        else: i += 1\n    return out\n'),
 ('valleys-too', 'peaks and troughs', 'def local_peaks(xs):\n    return [i for i in range(1, len(xs) - 1) if (xs[i] - xs[i - 1]) * (xs[i + 1] - xs[i]) < 0]\n'),
 ('abs', 'compares sizes', 'def local_peaks(xs):\n    return [i for i in range(1, len(xs) - 1) if abs(xs[i - 1]) < abs(xs[i]) > abs(xs[i + 1])]\n'),
]

C['at-search-smallest-n'] = [
 ('float-formula', 'ceil((-1 + sqrt(1 + 8t)) / 2) in floats', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    return math.ceil((-1 + math.sqrt(1 + 8 * target)) / 2)\n'),
 ('alt:float-formula-up-only', 'int of the float root, then one step up if short: right on every target tried near 10**18 (proposed_code.py)', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    n = int((math.sqrt(8 * target + 1) - 1) / 2)\n    return n if n * (n + 1) // 2 >= target else n + 1\n'),
 ('float-halving', 'halving with n * (n + 1) / 2 in floats', 'def rows_needed(target):\n    lo, hi = 0, 2 * 10**9\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if mid * (mid + 1) / 2 >= target: hi = mid\n        else: lo = mid + 1\n    return lo\n'),
 ('count-up', 'adds one row at a time', 'def rows_needed(target):\n    n = total = 0\n    while total < target:\n        n += 1; total += n\n    return n\n'),
 ('hi-too-small', 'halving up to 10**9', 'def rows_needed(target):\n    lo, hi = 0, 10**9\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if mid * (mid + 1) // 2 >= target: hi = mid\n        else: lo = mid + 1\n    return lo\n'),
 ('strict', 'more than target coins', 'def rows_needed(target):\n    lo, hi = 0, 2 * 10**9\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if mid * (mid + 1) // 2 > target: hi = mid\n        else: lo = mid + 1\n    return lo\n'),
 ('no-negative', 'isqrt of a negative number', 'import math\ndef rows_needed(target):\n    n = (math.isqrt(8 * target + 1) - 1) // 2\n    return n if n * (n + 1) // 2 >= target else n + 1\n'),
 ('largest-not-over', 'the largest n whose triangle fits in target', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    return (math.isqrt(8 * target + 1) - 1) // 2\n'),
 ('sqrt-2t', 'round(sqrt(2 t))', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    return round(math.sqrt(2 * target))\n'),
 ('lo-starts-at-one', 'halving from 1', 'def rows_needed(target):\n    lo, hi = 1, 2 * 10**9\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if mid * (mid + 1) // 2 >= target: hi = mid\n        else: lo = mid + 1\n    return lo\n'),
 ('float-then-walk-down-only', 'float root rounded up, corrected downwards only', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    n = math.ceil((math.sqrt(8 * target + 1) - 1) / 2)\n    while n > 0 and (n - 1) * n // 2 >= target: n -= 1\n    return n\n'),
 ('alt:isqrt', 'integer square root with a check', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    n = (math.isqrt(8 * target + 1) - 1) // 2\n    return n if n * (n + 1) // 2 >= target else n + 1\n'),
 ('alt:float-fixed-both-ways', 'float root as a first guess, then corrected up and down in whole numbers', 'import math\ndef rows_needed(target):\n    if target <= 0: return 0\n    n = int(math.sqrt(2 * target))\n    while n * (n + 1) // 2 < target: n += 1\n    while n > 0 and (n - 1) * n // 2 >= target: n -= 1\n    return n\n'),
]

C['at-search-count-in-range'] = [
 ('no-guard', 'negative when hi is below lo', 'from bisect import bisect_left, bisect_right\ndef count_in_range(xs, lo, hi):\n    return bisect_right(xs, hi) - bisect_left(xs, lo)\n'),
 ('left-left', 'bisect_left at both ends: values equal to hi lost', 'from bisect import bisect_left\ndef count_in_range(xs, lo, hi):\n    return max(0, bisect_left(xs, hi) - bisect_left(xs, lo))\n'),
 ('right-right', 'bisect_right at both ends: values equal to lo lost', 'from bisect import bisect_right\ndef count_in_range(xs, lo, hi):\n    return max(0, bisect_right(xs, hi) - bisect_right(xs, lo))\n'),
 ('linear', 'one pass over xs', 'def count_in_range(xs, lo, hi):\n    return sum(1 for x in xs if lo <= x <= hi)\n'),
 ('halve-then-walk', 'bisect for lo, then walks to hi', 'from bisect import bisect_left\ndef count_in_range(xs, lo, hi):\n    i = bisect_left(xs, lo); n = 0\n    while i < len(xs) and xs[i] <= hi: n += 1; i += 1\n    return n\n'),
 ('strict', 'lo < x < hi', 'from bisect import bisect_left, bisect_right\ndef count_in_range(xs, lo, hi):\n    return max(0, bisect_left(xs, hi) - bisect_right(xs, lo))\n'),
 ('plus-one', 'index difference plus one', 'from bisect import bisect_left\ndef count_in_range(xs, lo, hi):\n    if hi < lo or not xs: return 0\n    return bisect_left(xs, hi) - bisect_left(xs, lo) + 1\n'),
 ('own-halving-off-by-one', 'own halving that never looks past the last element', 'def count_in_range(xs, lo, hi):\n    def first(v):\n        a, b = 0, len(xs) - 1\n        while a < b:\n            m = (a + b) // 2\n            if xs[m] >= v: b = m\n            else: a = m + 1\n        return a\n    if hi < lo or not xs: return 0\n    return max(0, first(hi + 1) - first(lo))\n'),
 ('slice-walk', 'slices from the left edge and counts by walking', 'from bisect import bisect_left\ndef count_in_range(xs, lo, hi):\n    return len([x for x in xs[bisect_left(xs, lo):] if x <= hi])\n'),
 ('index-method', 'xs.index(lo) for the left edge', 'from bisect import bisect_right\ndef count_in_range(xs, lo, hi):\n    if hi < lo: return 0\n    try: i = xs.index(lo)\n    except ValueError: i = bisect_right(xs, lo)\n    return bisect_right(xs, hi) - i\n'),
 ('set-lookup', 'counts whole numbers from lo to hi that are in a set of xs', 'def count_in_range(xs, lo, hi):\n    s = set(xs)\n    return sum(1 for v in range(lo, hi + 1) if v in s)\n'),
 ('alt:hi-plus-one', 'bisect_left(hi + 1), right for whole numbers', 'from bisect import bisect_left\ndef count_in_range(xs, lo, hi):\n    return max(0, bisect_left(xs, hi + 1) - bisect_left(xs, lo))\n'),
 ('slice-len', 'len of the slice between the two bisects: right values, but the slice is a copy, so not O(log n)', 'from bisect import bisect_left, bisect_right\ndef count_in_range(xs, lo, hi):\n    return len(xs[bisect_left(xs, lo):bisect_right(xs, hi)])\n'),
]

C['gd-dp-walk-above-zero'] = [
 ('float-ballot', 'ballot formula with float division', 'from math import comb\ndef nonneg_walk_counts(n):\n    out = {}\n    for k in range(n % 2, n + 1, 2):\n        u = (n + k) // 2\n        out[k] = int(comb(n, u) * (k + 1) / (u + 1))\n    return out\n'),
 ('may-go-below', 'no floor at zero', 'from math import comb\ndef nonneg_walk_counts(n):\n    return {k: comb(n, (n + k) // 2) for k in range(n % 2, n + 1, 2)}\n'),
 ('zero-keys', 'a table with every position from 0 to n, zeros included', 'def nonneg_walk_counts(n):\n    c = [0] * (n + 2); c[0] = 1\n    for _ in range(n):\n        d = [0] * (n + 2)\n        for p in range(n + 1):\n            if c[p]:\n                d[p + 1] += c[p]\n                if p: d[p - 1] += c[p]\n        c = d\n    return {p: c[p] for p in range(n + 1)}\n'),
 ('enumerate', 'lists every walk', 'from itertools import product\ndef nonneg_walk_counts(n):\n    out = {}\n    for w in product((1, -1), repeat=n):\n        p = 0\n        for s in w:\n            p += s\n            if p < 0: break\n        else: out[p] = out.get(p, 0) + 1\n    return out\n'),
 ('plain-recursion', 'recursion with no memory', 'def nonneg_walk_counts(n):\n    out = {}\n    def go(k, p):\n        if p < 0: return\n        if k == n: out[p] = out.get(p, 0) + 1; return\n        go(k + 1, p + 1); go(k + 1, p - 1)\n    go(0, 0)\n    return out\n'),
 ('strictly-positive', 'never returns to 0 after the start', 'def nonneg_walk_counts(n):\n    c = {0: 1}\n    for i in range(n):\n        d = {}\n        for p, w in c.items():\n            for s in (1, -1):\n                q = p + s\n                if q > 0: d[q] = d.get(q, 0) + w\n        c = d\n    return c\n'),
 ('reflection-off-by-one', 'reflection with C(n, u + 2)', 'from math import comb\ndef nonneg_walk_counts(n):\n    out = {}\n    for k in range(n % 2, n + 1, 2):\n        u = (n + k) // 2\n        out[k] = comb(n, u) - (comb(n, u + 2) if u + 2 <= n else 0)\n    return out\n'),
 ('n-plus-one-steps', 'one step too many', 'def nonneg_walk_counts(n):\n    c = {0: 1}\n    for _ in range(n + 1):\n        d = {}\n        for p, w in c.items():\n            d[p + 1] = d.get(p + 1, 0) + w\n            if p: d[p - 1] = d.get(p - 1, 0) + w\n        c = d\n    return c\n'),
 ('float-counts', 'counts kept as floats', 'def nonneg_walk_counts(n):\n    c = {0: 1.0}\n    for _ in range(n):\n        d = {}\n        for p, w in c.items():\n            d[p + 1] = d.get(p + 1, 0) + w\n            if p: d[p - 1] = d.get(p - 1, 0) + w\n        c = d\n    return c\n'),
 ('true-division-catalan', 'ballot formula with / and int()', 'from math import comb\ndef nonneg_walk_counts(n):\n    out = {}\n    for k in range(n % 2, n + 1, 2):\n        u = (n + k) // 2\n        out[k] = int(comb(n, u) / (u + 1) * (k + 1))\n    return out\n'),
 ('alt:ballot-exact', 'reflection in whole numbers', 'from math import comb\ndef nonneg_walk_counts(n):\n    out = {}\n    for k in range(n % 2, n + 1, 2):\n        u = (n + k) // 2\n        out[k] = comb(n, u) - (comb(n, u + 1) if u + 1 <= n else 0)\n    return out\n'),
 ('alt:lru-cache', 'top-down with lru_cache', 'from functools import lru_cache\ndef nonneg_walk_counts(n):\n    @lru_cache(None)\n    def f(k, p):\n        if p < 0 or p > k: return 0\n        if k == 0: return 1 if p == 0 else 0\n        return f(k - 1, p - 1) + f(k - 1, p + 1)\n    return {p: f(n, p) for p in range(n % 2, n + 1, 2)}\n'),
]

C['pf-idioms-trend-direction'] = [
 ('ends-only', 'compares first and last', 'def trend(xs):\n    if len(xs) < 2: return 0\n    return 1 if xs[-1] > xs[0] else -1 if xs[-1] < xs[0] else 0\n'),
 ('first-and-last-pairs', 'checks the first pair and the last pair', 'def trend(xs):\n    if len(xs) < 2: return 0\n    if xs[0] < xs[1] and xs[-2] < xs[-1]: return 1\n    if xs[0] > xs[1] and xs[-2] > xs[-1]: return -1\n    return 0\n'),
 ('non-strict', 'sorted(xs) == xs', 'def trend(xs):\n    if len(xs) < 2: return 0\n    if xs == sorted(xs): return 1\n    if xs == sorted(xs, reverse=True): return -1\n    return 0\n'),
 ('no-short-guard', 'all() of nothing is True', 'def trend(xs):\n    if all(a < b for a, b in zip(xs, xs[1:])): return 1\n    if all(a > b for a, b in zip(xs, xs[1:])): return -1\n    return 0\n'),
 ('any', 'any pair rising', 'def trend(xs):\n    if any(a < b for a, b in zip(xs, xs[1:])): return 1\n    if any(a > b for a, b in zip(xs, xs[1:])): return -1\n    return 0\n'),
 ('majority', 'more rises than falls', 'def trend(xs):\n    up = sum(1 for a, b in zip(xs, xs[1:]) if a < b); dn = sum(1 for a, b in zip(xs, xs[1:]) if a > b)\n    return (up > dn) - (dn > up)\n'),
 ('no-falls', 'rising means no pair falls (and some pair rises)', 'def trend(xs):\n    up = any(a < b for a, b in zip(xs, xs[1:])); dn = any(a > b for a, b in zip(xs, xs[1:]))\n    return 1 if up and not dn else -1 if dn and not up else 0\n'),
 ('first-pair-sets-it', 'returns on the first pair', 'def trend(xs):\n    for a, b in zip(xs, xs[1:]):\n        if a < b: return 1\n        if a > b: return -1\n    return 0\n'),
 ('every-other', 'compares xs[i] with xs[i + 2]', 'def trend(xs):\n    if len(xs) < 2: return 0\n    if len(xs) == 2: return (xs[1] > xs[0]) - (xs[1] < xs[0])\n    if all(a < b for a, b in zip(xs, xs[2:])) and xs[0] < xs[1]: return 1\n    if all(a > b for a, b in zip(xs, xs[2:])) and xs[0] > xs[1]: return -1\n    return 0\n'),
 ('rising-only', 'never returns -1', 'def trend(xs):\n    if len(xs) < 2: return 0\n    return 1 if all(a < b for a, b in zip(xs, xs[1:])) else 0\n'),
 ('max-min-at-ends', 'the largest is last and the smallest first', 'def trend(xs):\n    if len(xs) < 2: return 0\n    if xs[-1] == max(xs) and xs[0] == min(xs) and xs[0] != xs[-1]: return 1\n    if xs[0] == max(xs) and xs[-1] == min(xs) and xs[0] != xs[-1]: return -1\n    return 0\n'),
 ('recursive', 'recursion over the list', 'def trend(xs):\n    if len(xs) < 2: return 0\n    def up(i): return i >= len(xs) - 1 or (xs[i] < xs[i + 1] and up(i + 1))\n    def dn(i): return i >= len(xs) - 1 or (xs[i] > xs[i + 1] and dn(i + 1))\n    return 1 if up(0) else -1 if dn(0) else 0\n'),
 ('alt:sorted-set', 'xs == sorted(set(xs))', 'def trend(xs):\n    if len(xs) < 2: return 0\n    if xs == sorted(set(xs)): return 1\n    if xs == sorted(set(xs), reverse=True): return -1\n    return 0\n'),
]

C['edge-case-list-to-pence'] = [
 ('float-int', 'int(float * 100)', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    return int(float(s) * 100)\n'),
 ('float-half-up', 'int(float * 100 + 0.5)', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    return int(float(s) * 100 + 0.5)\n'),
 ('float-result', 'right value as a float', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    return float(round(float(s) * 100))\n'),
 ('negative-pence-added', 'int(pounds) * 100 + pence with the sign left on the pounds', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    p, _, d = s.partition(".")\n    return int(p or "0") * 100 + int((d + "00")[:2])\n'),
 ('no-pad', 'one decimal place read as pence', 'def to_pence(text):\n    s = text.strip()\n    sign = -1 if s.startswith("-") else 1\n    s = s.lstrip("-").replace("£", "").replace(",", "")\n    p, _, d = s.partition(".")\n    return sign * (int(p or "0") * 100 + int(d or "0"))\n'),
 ('drop-the-point', 'removes the point and reads the digits', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    return int(s.replace(".", "")) if "." in s else int(s) * 100\n'),
 ('no-commas', 'commas left in', 'def to_pence(text):\n    s = text.strip()\n    sign = -1 if s.startswith("-") else 1\n    s = s.lstrip("-").replace("£", "")\n    p, _, d = s.partition(".")\n    return sign * (int(p or "0") * 100 + int((d + "00")[:2]))\n'),
 ('sign-before-strip', 'reads the pounds with their sign and adds the pence, guarded by a minus test made before stripping', 'def to_pence(text):\n    neg = text.startswith("-")\n    s = text.replace("£", "").replace(",", "").strip()\n    p, _, d = s.partition(".")\n    pence = int((d + "00")[:2])\n    if neg: return -(abs(int(p or "0")) * 100 + pence)\n    return int(p or "0") * 100 + pence\n'),
 ('no-strip-at-all', 'no strip: looks for the minus at index 0', 'def to_pence(text):\n    s = text\n    sign = -1 if s[:1] == "-" else 1\n    if sign < 0: s = s[1:]\n    s = s.replace("£", "").replace(",", "")\n    p, _, d = s.partition(".")\n    return sign * (int(p or "0") * 100 + int((d.strip() + "00")[:2]))\n'),
 ('pound-first-only', 'expects the £ sign first, so "-£" is not handled', 'def to_pence(text):\n    s = text.strip()\n    if s.startswith("£"): s = s[1:]\n    s = s.replace(",", "")\n    sign = -1 if s.startswith("-") else 1\n    p, _, d = s.lstrip("-").partition(".")\n    return sign * (int(p or "0") * 100 + int((d + "00")[:2]))\n'),
 ('alt:round-float', 'round(float * 100): right for every two-place price a float holds to within half a penny', 'def to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    return round(float(s) * 100)\n'),
 ('alt:decimal', 'Decimal', 'from decimal import Decimal\ndef to_pence(text):\n    s = text.strip().replace("£", "").replace(",", "")\n    return int(Decimal(s) * 100)\n'),
]

C['at-greedy-orders-to-fill'] = [
 ('book-order', 'takes the orders as they sit', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    t = 0\n    for n, s in enumerate(sizes, 1):\n        t += s\n        if t >= target: return n\n    return -1\n'),
 ('smallest-first', 'ascending', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    t = 0\n    for n, s in enumerate(sorted(sizes), 1):\n        t += s\n        if t >= target: return n\n    return -1\n'),
 ('strict', 'more than the target', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    t = 0\n    for n, s in enumerate(sorted(sizes, reverse=True), 1):\n        t += s\n        if t > target: return n\n    return -1\n'),
 ('no-zero-guard', 'target 0 takes one order', 'def orders_to_fill(sizes, target):\n    t = 0\n    for n, s in enumerate(sorted(sizes, reverse=True), 1):\n        t += s\n        if t >= target: return n\n    return -1\n'),
 ('no-minus-one', 'returns the count of all orders when short', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    t = n = 0\n    for s in sorted(sizes, reverse=True):\n        t += s; n += 1\n        if t >= target: break\n    return n\n'),
 ('max-and-remove', 'max and remove each round', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    left = list(sizes); t = n = 0\n    while left:\n        m = max(left); left.remove(m); t += m; n += 1\n        if t >= target: return n\n    return -1\n'),
 ('ceil-over-max', 'target over the largest order', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    if sum(sizes) < target: return -1\n    return -(-target // max(sizes))\n'),
 ('exact-only', 'wants the sizes to add to exactly the target', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    t = 0\n    for n, s in enumerate(sorted(sizes, reverse=True), 1):\n        t += s\n        if t == target: return n\n    return -1\n'),
 ('zero-when-short', 'returns 0 when short', 'def orders_to_fill(sizes, target):\n    t = 0\n    if target <= 0: return 0\n    for n, s in enumerate(sorted(sizes, reverse=True), 1):\n        t += s\n        if t >= target: return n\n    return 0\n'),
 ('prefix-sums-each-time', 'sum of the first n for each n', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    s = sorted(sizes, reverse=True)\n    for n in range(1, len(s) + 1):\n        if sum(s[:n]) >= target: return n\n    return -1\n'),
 ('alt:pop-front', 'sorted, then pop(0) each round: right, quadratic in memory moves only', 'def orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    left = sorted(sizes, reverse=True); t = n = 0\n    while left:\n        t += left.pop(0); n += 1\n        if t >= target: return n\n    return -1\n'),
 ('alt:heap', 'heapq', 'import heapq\ndef orders_to_fill(sizes, target):\n    if target <= 0: return 0\n    h = [-s for s in sizes]; heapq.heapify(h); t = n = 0\n    while h:\n        t -= heapq.heappop(h); n += 1\n        if t >= target: return n\n    return -1\n'),
]

C['pf-functions-binom-tail'] = [
 ('more-than-k', 'strictly more than k heads', 'from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    k = max(k, -1)\n    return Fraction(sum(comb(n, j) for j in range(k + 1, n + 1)), 2 ** n)\n'),
 ('float', 'a float', 'from math import comb\ndef binom_tail(n, k):\n    return sum(comb(n, j) for j in range(max(k, 0), n + 1)) / 2 ** n\n'),
 ('fraction-of-float', 'Fraction of a float sum', 'from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return Fraction(sum(comb(n, j) / 2 ** n for j in range(max(k, 0), n + 1)))\n'),
 ('negative-k', 'comb with a negative j', 'from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return Fraction(sum(comb(n, j) for j in range(k, n + 1)), 2 ** n)\n'),
 ('at-most', 'at most k heads', 'from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return Fraction(sum(comb(n, j) for j in range(0, min(k, n) + 1)), 2 ** n)\n'),
 ('exactly', 'exactly k heads', 'from fractions import Fraction\nfrom math import comb\ndef binom_tail(n, k):\n    return Fraction(comb(n, k) if 0 <= k <= n else 0, 2 ** n)\n'),
]
