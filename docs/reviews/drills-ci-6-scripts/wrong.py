"""Wrong or too-slow solutions a real candidate writes, none of them planted by
the author. harness.py runs each against every example and hidden test.
CANDIDATES = {label: (drill id, source, what the slip is)}.
A label ending in '(right)' is a correct solution by another method, kept to
show the tests accept it."""

C = {}

# ---------------------------------------------------------------- best session
C['session: latest lowest prefix'] = ('ci-best-session', '''
def best_session(pnl):
    best = None
    low, low_at, pre = 0, 0, 0
    for j, x in enumerate(pnl):
        pre += x
        if best is None or pre - low > best[0]:
            best = [pre - low, low_at, j]
        if pre <= low:
            low, low_at = pre, j + 1
    return best
''', 'a later equal prefix replaces the lowest, so the start is the latest')

C['session: every run'] = ('ci-best-session', '''
def best_session(pnl):
    best = None
    n = len(pnl)
    for s in range(n):
        tot = 0
        for e in range(s, n):
            tot += pnl[e]
            if best is None or tot > best[0]:
                best = [tot, s, e]
    return best
''', 'O(n^2)')

C['session: total by Kadane, then a scan from each start'] = ('ci-best-session', '''
def best_session(pnl):
    run = top = pnl[0]
    for x in pnl[1:]:
        run = max(x, run + x)
        top = max(top, run)
    for s in range(len(pnl)):
        tot = 0
        for e in range(s, len(pnl)):
            tot += pnl[e]
            if tot == top:
                return [top, s, e]
''', 'right answer, O(n^2) when the best run starts late')

C['session: zeros trimmed from the front'] = ('ci-best-session', '''
def best_session(pnl):
    best = [pnl[0], 0, 0]
    run, start = pnl[0], 0
    for i in range(1, len(pnl)):
        if run >= 0:
            run += pnl[i]
        else:
            run, start = pnl[i], i
        if run > best[0]:
            best = [run, start, i]
    t, s, e = best
    while s < e and pnl[s] == 0:
        s += 1
    return [t, s, e]
''', 'drops leading zero days to make the run shorter, against "earliest start" first')

# ---------------------------------------------------------------- broken steps
C['steps: modulus only at the end'] = ('ci-broken-steps', '''
def ways_up(n, broken):
    bad = set(broken)
    a, b, c = 0, 0, 1
    for i in range(1, n + 1):
        a, b, c = b, c, (0 if i in bad else a + b + c)
    return c % 1_000_000_007
''', 'exact integers of 26,000 digits; right value, slow')

C['steps: broken kept as a list'] = ('ci-broken-steps', '''
def ways_up(n, broken):
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        if i in broken:
            continue
        ways[i] = sum(ways[max(0, i - 3):i]) % 1_000_000_007
    return ways[n]
''', 'a list lookup per step, O(n * b)')

C['steps: last step never checked'] = ('ci-broken-steps', '''
def ways_up(n, broken):
    bad = set(broken)
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(0, n):
        if i in bad:
            continue
        for d in (1, 2, 3):
            if i + d <= n:
                ways[i + d] = (ways[i + d] + ways[i]) % 1_000_000_007
    return ways[n]
''', 'pushes counts forward from sound steps, so a cracked top step still collects')

# ---------------------------------------------------------------- shift picks
C['shifts: tie keeps the rest-day plan'] = ('ci-shift-picks', '''
def best_shifts(pay):
    n = len(pay)
    total = [0] * (n + 2)
    days = [0] * (n + 2)
    for i, x in enumerate(pay):
        if total[i] + x > total[i + 1]:
            total[i + 2], days[i + 2] = total[i] + x, days[i] + 1
        else:
            total[i + 2], days[i + 2] = total[i + 1], days[i + 1]
    return [total[-1], days[-1]]
''', 'on equal pay keeps the plan that rests, without comparing the day counts')

C['shifts: richest day first'] = ('ci-shift-picks', '''
def best_shifts(pay):
    n = len(pay)
    used = [False] * (n + 2)
    total = days = 0
    for i in sorted(range(n), key=lambda i: -pay[i]):
        if pay[i] and not used[i] and not used[i + 2]:
            used[i + 1] = True
            total += pay[i]
            days += 1
    return [total, days]
''', 'greedy by pay')

C['shifts: days counted from a plan walked back'] = ('ci-shift-picks', '''
def best_shifts(pay):
    n = len(pay)
    best = [0] * (n + 2)
    for i, x in enumerate(pay):
        best[i + 2] = max(best[i + 1], best[i] + x)
    i, days = n - 1, 0
    while i >= 0:
        if best[i + 2] == best[i + 1]:
            i -= 1
        else:
            days += 1
            i -= 2
    return [best[-1], days]
''', 'one best plan rebuilt preferring to rest; not always the fewest days')

# ---------------------------------------------------------------- ring stalls
C['ring: three rows (right)'] = ('ci-ring-stalls', '''
def best_rent(rents):
    n = len(rents)
    if n <= 3:
        return max(rents)
    def row(lo, hi):
        a = b = c = 0
        for i in range(lo, hi + 1):
            a, b, c = b, c, max(c, a + rents[i])
        return c
    return max(row(0, n - 3), row(1, n - 2), row(2, n - 1))
''', 'right: some two neighbours among n-2, n-1, 0, 1 are empty')

C['ring: two rows as the one-gap ring'] = ('ci-ring-stalls', '''
def best_rent(rents):
    n = len(rents)
    if n <= 3:
        return max(rents)
    def row(lo, hi):
        a = b = c = 0
        for i in range(lo, hi + 1):
            a, b, c = b, c, max(c, a + rents[i])
        return c
    return max(row(0, n - 2), row(1, n - 1))
''', 'drops one end stall, which leaves 0 and n-2 or 1 and n-1 too close')

C['ring: first stall 0, 1 or 2 only'] = ('ci-ring-stalls', '''
def best_rent(rents):
    n = len(rents)
    if n <= 3:
        return max(rents)
    def row(lo, hi):
        a = b = c = 0
        for i in range(lo, hi + 1):
            a, b, c = b, c, max(c, a + rents[i])
        return c
    return max(rents[k] + row(k + 3, n - 3 + k) for k in range(3))
''', 'forgets the case with none of 0, 1, 2 let')

C['ring: stall 0 rules out only one stall behind'] = ('ci-ring-stalls', '''
def best_rent(rents):
    n = len(rents)
    if n <= 3:
        return max(rents)
    def row(lo, hi):
        a = b = c = 0
        for i in range(lo, hi + 1):
            a, b, c = b, c, max(c, a + rents[i])
        return c
    return max(rents[0] + row(3, n - 2), rents[1] + row(4, n - 2), row(2, n - 1))
''', 'with stall 0 let, stall n-2 stays open')

C['ring: no small ring case'] = ('ci-ring-stalls', '''
def best_rent(rents):
    n = len(rents)
    def row(lo, hi):
        a = b = c = 0
        for i in range(max(lo, 0), hi + 1):
            a, b, c = b, c, max(c, a + rents[i])
        return c
    return max(row(0, n - 3), row(1, n - 2), row(2, n - 1))
''', 'three rows without the n <= 3 case')

# ---------------------------------------------------------------- change ways
C['ways: a table per different fare'] = ('ci-change-ways', '''
def solve_change_ways(text):
    tok = text.split()
    k = int(tok[0])
    coins = [int(t) for t in tok[1:1 + k]]
    q = int(tok[1 + k])
    memo = {}
    out = []
    for f in map(int, tok[2 + k:2 + k + q]):
        if f not in memo:
            ways = [1] + [0] * f
            for c in coins:
                for a in range(c, f + 1):
                    ways[a] = (ways[a] + ways[a - c]) % 1_000_000_007
            memo[f] = ways[f]
        out.append(str(memo[f]))
    return '\\n'.join(out)
''', 'the ruled-out method with a memo on the fare')

C['ways: fares read from the fourth line only'] = ('ci-change-ways', '''
def solve_change_ways(text):
    lines = [x for x in text.split('\\n') if x.strip()]
    coins = [int(t) for t in lines[1].split()]
    fares = [int(t) for t in lines[3].split()]
    top = max(fares)
    ways = [1] + [0] * top
    for c in coins:
        for a in range(c, top + 1):
            ways[a] = (ways[a] + ways[a - c]) % 1_000_000_007
    return '\\n'.join(str(ways[f]) for f in fares)
''', 'the fares may run over several lines')

C['ways: memo on (coin, amount) recursion'] = ('ci-change-ways', '''
import sys
from functools import lru_cache
def solve_change_ways(text):
    sys.setrecursionlimit(100000)
    tok = text.split()
    k = int(tok[0])
    coins = [int(t) for t in tok[1:1 + k]]
    q = int(tok[1 + k])
    @lru_cache(None)
    def go(i, left):
        if left == 0:
            return 1
        if i == k or left < 0:
            return 0
        return (go(i, left - coins[i]) + go(i + 1, left)) % 1_000_000_007
    return '\\n'.join(str(go(0, int(f))) for f in tok[2 + k:2 + k + q])
''', 'top-down; 400,000 states and deep recursion')

# ---------------------------------------------------------------- product stretch
C['product: every stretch'] = ('ci-product-stretch', '''
def best_product_stretch(factors):
    best = None
    n = len(factors)
    for s in range(n - 1):
        p = factors[s]
        for e in range(s + 1, n):
            p *= factors[e]
            if best is None or p > best:
                best = p
    return best
''', 'the method constraints[1] calls slow')

C['product: zero-free pieces, short remainders allowed'] = ('ci-product-stretch', '''
def best_product_stretch(factors):
    best = 0 if 0 in factors else None
    piece = []
    def close():
        nonlocal best
        if len(piece) < 2:
            return
        p = 1
        for x in piece:
            p *= x
        cands = [p]
        if p < 0:
            i = next(i for i, x in enumerate(piece) if x < 0)
            j = max(i for i, x in enumerate(piece) if x < 0)
            a = 1
            for x in piece[i + 1:]:
                a *= x
            b = 1
            for x in piece[:j]:
                b *= x
            cands = [a, b]
        m = max(cands)
        if best is None or m > best:
            best = m
    for x in factors:
        if x == 0:
            close()
            piece = []
        else:
            piece.append(x)
    close()
    return best
''', 'after dropping up to the first negative, a remainder of one hour or none is still counted')

C['product: prefix and suffix products, zero forgotten'] = ('ci-product-stretch', '''
def best_product_stretch(factors):
    best = None
    for seq in (factors, factors[::-1]):
        p, length = 1, 0
        for x in seq:
            if x == 0:
                p, length = 1, 0
                continue
            p *= x
            length += 1
            if length >= 2 and (best is None or p > best):
                best = p
    if best is None:
        return 0
    return best
''', 'a stretch through a zero scores 0, which beats a negative best')

C['product: floats'] = ('ci-product-stretch', '''
def best_product_stretch(factors):
    hi = lo = float(factors[0])
    best = None
    for x in factors[1:]:
        a, b = hi * x, lo * x
        if best is None or max(a, b) > best:
            best = max(a, b)
        hi, lo = max(x, a, b), min(x, a, b)
    return int(best)
''', 'not exact past 2^53')

# ---------------------------------------------------------------- paving ways
C['paving: drains read as [col, row]'] = ('ci-paving-ways', '''
def paving_ways(n, drains):
    mod = 1_000_000_007
    blocked = [0] * max(n, 3)
    for c, r in drains:
        if c < len(blocked) and r < 3:
            blocked[c] |= 1 << r
    def fill(row, full, nxt, out):
        if row == 3:
            out.append(nxt); return
        bit = 1 << row
        if full & bit:
            fill(row + 1, full, nxt, out); return
        fill(row + 1, full | bit, nxt | bit, out)
        if row < 2 and not full & (bit << 1):
            fill(row + 2, full | bit | (bit << 1), nxt, out)
    moves = []
    for full in range(8):
        out = []; fill(0, full, 0, out); moves.append(out)
    ways = [1] + [0] * 7
    for c in range(n):
        new = [0] * 8
        b = blocked[c]
        for s in range(8):
            if ways[s] and not s & b:
                for nxt in moves[s | b]:
                    new[nxt] += ways[s]
        ways = [x % mod for x in new]
    return ways[0]
''', 'row and column swapped')

C['paving: a drain in the last column may be covered'] = ('ci-paving-ways', '''
def paving_ways(n, drains):
    mod = 1_000_000_007
    blocked = [0] * (n + 1)
    for r, c in drains:
        blocked[c] |= 1 << r
    def fill(row, full, nxt, out):
        if row == 3:
            out.append(nxt); return
        bit = 1 << row
        if full & bit:
            fill(row + 1, full, nxt, out); return
        fill(row + 1, full | bit, nxt | bit, out)
        if row < 2 and not full & (bit << 1):
            fill(row + 2, full | bit | (bit << 1), nxt, out)
    moves = []
    for full in range(8):
        out = []; fill(0, full, 0, out); moves.append(out)
    ways = [1] + [0] * 7
    for c in range(n):
        new = [0] * 8
        for s in range(8):
            if ways[s]:
                for nxt in moves[s | blocked[c]]:
                    if c + 1 < n - 1 and nxt & blocked[c + 1]:
                        continue
                    new[nxt] += ways[s]
        ways = [x % mod for x in new]
    return ways[0]
''', 'the overlap check stops one column short, so a slab can end on a drain in the last column')

C['paving: across slabs only checked against the state'] = ('ci-paving-ways', '''
def paving_ways(n, drains):
    mod = 1_000_000_007
    blocked = [0] * n
    for r, c in drains:
        blocked[c] |= 1 << r
    ways = [1] + [0] * 7
    for c in range(n):
        new = [0] * 8
        b = blocked[c]
        for s in range(8):
            if not ways[s] or s & b:
                continue
            free = 7 & ~(s | b)
            opts = [free]                      # all along
            if free & 3 == 3:
                opts.append(free & ~3)
            if free & 6 == 6:
                opts.append(free & ~6)
            for nxt in opts:
                new[nxt] += ways[s]
        ways = [x % mod for x in new]
    return ways[0]
''', 'right as far as I can see: three cells allow at most one across slab (right)')

C['paving: modulus only at the end'] = ('ci-paving-ways', '''
def paving_ways(n, drains):
    blocked = [0] * n
    for r, c in drains:
        blocked[c] |= 1 << r
    ways = [1] + [0] * 7
    for c in range(n):
        new = [0] * 8
        b = blocked[c]
        for s in range(8):
            if not ways[s] or s & b:
                continue
            free = 7 & ~(s | b)
            new[free] += ways[s]
            if free & 3 == 3:
                new[free & ~3] += ways[s]
            if free & 6 == 6:
                new[free & ~6] += ways[s]
        ways = new
    return ways[0] % 1_000_000_007
''', 'exact integers of thousands of digits; right value, slower')

# ---------------------------------------------------------------- cooldown trades
C['cooldown: no bound on the look-back'] = ('ci-cooldown-trades', '''
def cooldown_profit(prices, k):
    n = len(prices)
    cash = [0] * n
    hold = -prices[0]
    for i in range(1, n):
        hold = max(hold, cash[i - k - 1] - prices[i])
        cash[i] = max(cash[i - 1], hold + prices[i])
    return cash[-1]
''', 'a negative index wraps to a later, still zero, entry; IndexError once k is n + 1 or more')

C['cooldown: a rest counter per state'] = ('ci-cooldown-trades', '''
def cooldown_profit(prices, k):
    NEG = float('-inf')
    hold = NEG
    rest = [NEG] * (k + 1)     # rest[j]: no share, j rest days still to sit out
    rest[0] = 0
    for p in prices:
        new = [NEG] * (k + 1)
        new_hold = max(hold, rest[0] - p)
        new[0] = rest[0]
        for j in range(1, k + 1):
            if rest[j] > new[j - 1]:
                new[j - 1] = rest[j]
        if hold + p > new[k]:
            new[k] = hold + p
        hold, rest = new_hold, new
    return max(rest)
''', 'O(n * k)')

C['cooldown: every buy day for each sale'] = ('ci-cooldown-trades', '''
def cooldown_profit(prices, k):
    n = len(prices)
    cash = [0] * n
    for i in range(1, n):
        best = cash[i - 1]
        for b in range(i):
            base = cash[b - k - 1] if b - k - 1 >= 0 else 0
            if base + prices[i] - prices[b] > best:
                best = base + prices[i] - prices[b]
        cash[i] = best
    return cash[-1]
''', 'O(n^2)')

C['cooldown: rest counted from the day after the sale'] = ('ci-cooldown-trades', '''
def cooldown_profit(prices, k):
    n = len(prices)
    cash = [0] * n
    hold = -prices[0]
    for i in range(1, n):
        cash[i] = max(cash[i - 1], hold + prices[i])
        back = cash[i - k] if i - k >= 0 else 0
        if k > 0:
            hold = max(hold, (cash[i - k - 1] if i - k - 1 >= 0 else 0) - prices[i])
        else:
            hold = max(hold, back - prices[i])
    return cash[-1]
''', 'with k = 0 the sale and the next buy share a day, which changes nothing (right)')

# ---------------------------------------------------------------- word split
C['words: every code tried at every position'] = ('ci-word-split', '''
def fewest_words(text, words):
    n = len(text)
    big = n + 1
    best = [0] + [big] * n
    for i in range(n):
        if best[i] == big:
            continue
        for w in words:
            if text.startswith(w, i) and best[i] + 1 < best[i + len(w)]:
                best[i + len(w)] = best[i] + 1
    return best[n] if best[n] < big else -1
''', 'O(n * number of codes), not O(n * L)')

C['words: memo recursion at the default depth'] = ('ci-word-split', '''
from functools import lru_cache
def fewest_words(text, words):
    vocab = set(words)
    lens = sorted({len(w) for w in words})
    n = len(text)
    @lru_cache(None)
    def go(i):
        if i == n:
            return 0
        best = n + 1
        for L in lens:
            if i + L <= n and text[i:i + L] in vocab:
                best = min(best, 1 + go(i + L))
        return best
    r = go(0)
    return r if r <= n else -1
''', 'the memo fixes the time but not the depth')

C['words: every earlier cut'] = ('ci-word-split', '''
def fewest_words(text, words):
    vocab = set(words)
    n = len(text)
    big = n + 1
    best = [0] + [big] * n
    for i in range(1, n + 1):
        for j in range(i):
            if best[j] + 1 < best[i] and text[j:i] in vocab:
                best[i] = best[j] + 1
    return best[n] if best[n] < big else -1
''', 'O(n^2) cuts')

C['words: every earlier cut within the longest code'] = ('ci-word-split', '''
def fewest_words(text, words):
    vocab = set(words)
    longest = max(map(len, words))
    n = len(text)
    big = n + 1
    best = [0] + [big] * n
    for i in range(1, n + 1):
        for j in range(max(0, i - longest), i):
            if best[j] + 1 < best[i] and text[j:i] in vocab:
                best[i] = best[j] + 1
    return best[n] if best[n] < big else -1
''', 'O(n * 20), right (right)')

# ---------------------------------------------------------------- longest rising
C['rising: tails scanned from the front'] = ('ci-longest-rising', '''
def rising_readings(readings):
    tails = []
    for x in readings:
        for k, t in enumerate(tails):
            if t >= x:
                tails[k] = x
                break
        else:
            tails.append(x)
    return [len(tails), tails[-1]]
''', 'O(n * length), no binary search')

C['rising: tails scanned from the back'] = ('ci-longest-rising', '''
def rising_readings(readings):
    tails = []
    for x in readings:
        k = len(tails)
        while k and tails[k - 1] >= x:
            k -= 1
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return [len(tails), tails[-1]]
''', 'O(n * length), no binary search')

C['rising: best chain per value in a dict'] = ('ci-longest-rising', '''
def rising_readings(readings):
    best = {}
    for x in readings:
        m = 0
        for v, l in best.items():
            if v < x and l > m:
                m = l
        if best.get(x, 0) < m + 1:
            best[x] = m + 1
    top = max(best.values())
    return [top, min(v for v, l in best.items() if l == top)]
''', 'O(n * different values)')

C['rising: end is the smallest reading of the last pile'] = ('ci-longest-rising', '''
from bisect import bisect_left
def rising_readings(readings):
    tails, firsts = [], []
    for x in readings:
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    return [len(tails), min(x for x in readings if x >= tails[-1]) if tails else 0]
''', 'returns tails[-1] by a roundabout route (right)')

# ---------------------------------------------------------------- tape decodes
C['tape: modulus only at the end'] = ('ci-tape-decodes', '''
def solve_tape_decodes(text):
    tok = text.split()
    out = []
    for tape in tok[1:1 + int(tok[0])]:
        prev, cur = 1, (9 if tape[0] == '?' else 0 if tape[0] == '0' else 1)
        for i in range(1, len(tape)):
            a, b = tape[i - 1], tape[i]
            one = 9 if b == '?' else 0 if b == '0' else 1
            if a == '1':
                two = 10 if b == '?' else 1
            elif a == '2':
                two = 7 if b == '?' else 1 if b <= '6' else 0
            elif a == '?':
                two = 17 if b == '?' else 2 if b <= '6' else 1
            else:
                two = 0
            prev, cur = cur, one * cur + two * prev
        out.append(str(cur % 1_000_000_007))
    return '\\n'.join(out)
''', 'exact integers; right value, slow')

C['tape: a smudge before 0 counted once'] = ('ci-tape-decodes', '''
def solve_tape_decodes(text):
    tok = text.split()
    out = []
    for tape in tok[1:1 + int(tok[0])]:
        prev, cur = 1, (9 if tape[0] == '?' else 0 if tape[0] == '0' else 1)
        for i in range(1, len(tape)):
            a, b = tape[i - 1], tape[i]
            one = 9 if b == '?' else 0 if b == '0' else 1
            if a == '1':
                two = 10 if b == '?' else 1
            elif a == '2':
                two = 7 if b == '?' else 1 if b <= '6' else 0
            elif a == '?':
                two = 17 if b == '?' else 2 if '1' <= b <= '6' else 1
            else:
                two = 0
            prev, cur = cur, (one * cur + two * prev) % 1_000_000_007
        out.append(str(cur))
    return '\\n'.join(out)
''', '?0 is 10 or 20')

C['tape: every fill of each pair, memo recursion'] = ('ci-tape-decodes', '''
from functools import lru_cache
def solve_tape_decodes(text):
    tok = text.split()
    out = []
    for tape in tok[1:1 + int(tok[0])]:
        n = len(tape)
        @lru_cache(None)
        def go(i):
            if i == n:
                return 1
            tot = (9 if tape[i] == '?' else 0 if tape[i] == '0' else 1) * go(i + 1)
            if i + 1 < n:
                c = 0
                for a in ('0123456789' if tape[i] == '?' else tape[i]):
                    for b in ('0123456789' if tape[i + 1] == '?' else tape[i + 1]):
                        c += 10 <= int(a + b) <= 26
                if c:
                    tot += c * go(i + 2)
            return tot % 1_000_000_007
        out.append(str(go(0)))
    return '\\n'.join(out)
''', 'the memo fixes the time but not the depth')

C['tape: one line per tape, read by t without skipping blanks'] = ('ci-tape-decodes', '''
def solve_tape_decodes(text):
    lines = text.split('\\n')
    t = int(lines[0])
    out = []
    for tape in lines[1:1 + t]:
        tape = tape.strip()
        prev, cur = 1, (9 if tape[0] == '?' else 0 if tape[0] == '0' else 1)
        for i in range(1, len(tape)):
            a, b = tape[i - 1], tape[i]
            one = 9 if b == '?' else 0 if b == '0' else 1
            if a == '1':
                two = 10 if b == '?' else 1
            elif a == '2':
                two = 7 if b == '?' else 1 if b <= '6' else 0
            elif a == '?':
                two = 17 if b == '?' else 2 if b <= '6' else 1
            else:
                two = 0
            prev, cur = cur, (one * cur + two * prev) % 1_000_000_007
        out.append(str(cur))
    return '\\n'.join(out)
''', 'right for the stated format: blank lines come only at the end (right)')

# ---------------------------------------------------------------- fewest tokens
C['tokens: first token found, then sorted'] = ('ci-fewest-tokens', '''
def fewest_tokens(values, amount):
    big = amount + 1
    need = [0] + [big] * amount
    last = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for v in values:
            if v <= a and need[a - v] + 1 < need[a]:
                need[a], last[a] = need[a - v] + 1, v
    if need[amount] == big:
        return []
    out, a = [], amount
    while a:
        out.append(last[a]); a -= last[a]
    return sorted(out, reverse=True)
''', 'the pointer keeps the first value in the given order, not the largest')

C['tokens: last token found in the given order'] = ('ci-fewest-tokens', '''
def fewest_tokens(values, amount):
    big = amount + 1
    need = [0] + [big] * amount
    last = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for v in values:
            if v <= a and need[a - v] + 1 <= need[a]:
                need[a], last[a] = need[a - v] + 1, v
    if need[amount] >= big:
        return []
    out, a = [], amount
    while a:
        out.append(last[a]); a -= last[a]
    return sorted(out, reverse=True)
''', 'right only when the values come in increasing order')

C['tokens: rebuild without the v <= a guard'] = ('ci-fewest-tokens', '''
def fewest_tokens(values, amount):
    big = amount + 1
    need = [0] + [big] * amount
    for a in range(1, amount + 1):
        for v in values:
            if v <= a and need[a - v] + 1 < need[a]:
                need[a] = need[a - v] + 1
    if need[amount] == big:
        return []
    order = sorted(values, reverse=True)
    out, a = [], amount
    while a > 0:
        for v in order:
            if need[a - v] == need[a] - 1:
                out.append(v); a -= v
                break
    return out
''', 'a - v below 0 reads the table from its far end')

C['tokens: largest first token, the rest by any pointer'] = ('ci-fewest-tokens', '''
def fewest_tokens(values, amount):
    big = amount + 1
    need = [0] + [big] * amount
    last = [0] * (amount + 1)
    for a in range(1, amount + 1):
        for v in sorted(values):
            if v <= a and need[a - v] + 1 < need[a]:
                need[a], last[a] = need[a - v] + 1, v
    if need[amount] == big:
        return []
    first = max(v for v in values if v <= amount and need[amount - v] == need[amount] - 1)
    out, a = [first], amount - first
    while a:
        out.append(last[a]); a -= last[a]
    return sorted(out, reverse=True)
''', 'the tie rule applied to the first token only')

C['tokens: the best list stored for every amount (right)'] = ('ci-fewest-tokens', '''
def fewest_tokens(values, amount):
    best = [()] + [None] * amount
    for a in range(1, amount + 1):
        top = None
        for v in values:
            if v <= a and best[a - v] is not None:
                p = best[a - v]
                if p and p[0] > v:
                    continue
                c = (v,) + p
                if top is None or len(c) < len(top) or (len(c) == len(top) and c > top):
                    top = c
        best[a] = top
    return list(best[amount] or [])
''', 'not right in general: skips a list whose head is above v; kept to see what the tests say')

# ---------------------------------------------------------------- long stairwell
C['stairwell: modulus only at the end'] = ('ci-long-stairwell', '''
def stride_ways(n, strides):
    m = max(strides)
    step = [[0] * m for _ in range(m)]
    for s in strides:
        step[0][s - 1] = 1
    for r in range(1, m):
        step[r][r - 1] = 1
    def mul(A, B):
        return [[sum(A[i][t] * B[t][j] for t in range(m)) for j in range(m)] for i in range(m)]
    result = [[int(i == j) for j in range(m)] for i in range(m)]
    while n:
        if n & 1:
            result = mul(result, step)
        step = mul(step, step)
        n >>= 1
    return result[0][0] % 1_000_000_007
''', 'the entries grow without bound')

C['stairwell: numpy int64 matrix power'] = ('ci-long-stairwell', '''
import numpy as np
def stride_ways(n, strides):
    mod = 1_000_000_007
    m = max(strides)
    step = np.zeros((m, m), dtype=np.int64)
    for s in strides:
        step[0, s - 1] = 1
    for r in range(1, m):
        step[r, r - 1] = 1
    result = np.eye(m, dtype=np.int64)
    while n:
        if n & 1:
            result = result @ step % mod
        step = step @ step % mod
        n >>= 1
    return int(result[0, 0])
''', 'eight products below 2^60 fit int64, so this is right (right)')

C['stairwell: first m counts, then the power on the rest'] = ('ci-long-stairwell', '''
def stride_ways(n, strides):
    mod = 1_000_000_007
    m = max(strides)
    f = [1] + [0] * (m - 1)
    for i in range(1, m):
        f[i] = sum(f[i - s] for s in strides if s <= i) % mod
    if n < m:
        return f[n]
    step = [[0] * m for _ in range(m)]
    for s in strides:
        step[0][s - 1] = 1
    for r in range(1, m):
        step[r][r - 1] = 1
    def mul(A, B):
        return [[sum(A[i][t] * B[t][j] for t in range(m)) % mod for j in range(m)] for i in range(m)]
    result = [[int(i == j) for j in range(m)] for i in range(m)]
    e = n - m
    while e:
        if e & 1:
            result = mul(result, step)
        step = mul(step, step)
        e >>= 1
    return sum(result[0][j] * f[m - 1 - j] for j in range(m)) % mod
''', 'power n - m where n - m + 1 is needed')

# ---------------------------------------------------------------- nested crates
C['crates: by height then width, strict widths (right)'] = ('ci-nested-crates', '''
from bisect import bisect_left
def longest_nest(crates):
    tails = []
    for h, w in sorted((h, w) for w, h in crates):
        k = bisect_left(tails, w)
        if k == len(tails):
            tails.append(w)
        else:
            tails[k] = w
    return len(tails)
''', 'right, and five lines: sort by (height, width) and take the longest strictly rising run of widths')

C['crates: usual trick on the set of crates (right)'] = ('ci-nested-crates', '''
from bisect import bisect_right
def longest_nest(crates):
    tails = []
    for w, h in sorted({(w, h) for w, h in crates}, key=lambda c: (c[0], -c[1])):
        k = bisect_right(tails, h)
        if k == len(tails):
            tails.append(h)
        else:
            tails[k] = h
    return len(tails)
''', 'right: the usual sort works once equal crates are dropped')

C['crates: tails scanned, no binary search'] = ('ci-nested-crates', '''
def longest_nest(crates):
    tails = []
    for h, w in sorted((h, w) for w, h in crates):
        for k, t in enumerate(tails):
            if t >= w:
                tails[k] = w
                break
        else:
            tails.append(w)
    return len(tails)
''', 'O(n * answer)')

C['crates: best row per height value'] = ('ci-nested-crates', '''
def longest_nest(crates):
    groups = {}
    for w, h in crates:
        groups.setdefault(w, set()).add(h)
    best = {}
    for w in sorted(groups):
        new = {}
        for h in groups[w]:
            m = 0
            for h2, l in best.items():
                if h2 <= h and l > m:
                    m = l
            new[h] = m + 1
        for h, l in new.items():
            if best.get(h, 0) < l:
                best[h] = l
    return max(best.values())
''', 'O(n * different heights)')

C['crates: by height then width, widths may repeat'] = ('ci-nested-crates', '''
from bisect import bisect_right
def longest_nest(crates):
    tails = []
    for h, w in sorted((h, w) for w, h in crates):
        k = bisect_right(tails, w)
        if k == len(tails):
            tails.append(w)
        else:
            tails[k] = w
    return len(tails)
''', 'equal widths chain')

C['crates: by width then height, heights from the group in rising order'] = ('ci-nested-crates', '''
from bisect import bisect_right
def longest_nest(crates):
    tails = []
    for w, h in sorted(map(tuple, crates)):
        k = bisect_right(tails, h)
        if k == len(tails):
            tails.append(h)
        else:
            tails[k] = h
    return len(tails)
''', 'equal widths chain')

# ---------------------------------------------------------------- capped trips
C['trips: every buy day for each sale'] = ('ci-capped-trips', '''
def best_trips(prices, k, fee):
    n = len(prices)
    prev = [0] * (n + 1)          # prev[i]: best with j - 1 trips inside the first i days
    for _ in range(k):
        cur = [0] * (n + 1)
        for s in range(1, n):
            best = cur[s]
            for b in range(s):
                g = prev[b] + prices[s] - prices[b] - fee
                if g > best:
                    best = g
            cur[s + 1] = best
        prev = cur
    return prev[n]
''', 'O(n^2 * k)')

C['trips: the usual shortcut for a large k, fee taken per rise'] = ('ci-capped-trips', '''
def best_trips(prices, k, fee):
    n = len(prices)
    if k >= n // 2:
        return sum(max(0, b - a - fee) for a, b in zip(prices, prices[1:]))
    hold = [float('-inf')] * (k + 1)
    free = [0] * (k + 1)
    for p in prices:
        for j in range(k, 0, -1):
            free[j] = max(free[j], hold[j] + p - fee)
            hold[j] = max(hold[j], free[j - 1] - p)
    return max(free)
''', 'with a fee, day-by-day rises are not the unlimited answer')

C['trips: the usual shortcut for a large k, fee per upward run'] = ('ci-capped-trips', '''
def best_trips(prices, k, fee):
    n = len(prices)
    if k >= n // 2:
        total, low = 0, prices[0]
        for a, b in zip(prices, prices[1:] + [0]):
            if b < a:
                total += max(0, a - low - fee)
                low = b
        return total
    hold = [float('-inf')] * (k + 1)
    free = [0] * (k + 1)
    for p in prices:
        for j in range(k, 0, -1):
            free[j] = max(free[j], hold[j] + p - fee)
            hold[j] = max(hold[j], free[j - 1] - p)
    return max(free)
''', 'with a fee, joining two runs across a small dip can beat taking both')

C['trips: answer read at exactly k trips'] = ('ci-capped-trips', '''
def best_trips(prices, k, fee):
    hold = [float('-inf')] * (k + 1)
    free = [0] + [float('-inf')] * k
    for p in prices:
        for j in range(k, 0, -1):
            free[j] = max(free[j], hold[j] + p - fee)
            hold[j] = max(hold[j], free[j - 1] - p)
    return max(0, free[k])
''', 'forces all k trips where fewer pay more')

C['trips: memo recursion at the default depth'] = ('ci-capped-trips', '''
from functools import lru_cache
def best_trips(prices, k, fee):
    n = len(prices)
    @lru_cache(None)
    def go(i, left, holding):
        if i == n:
            return 0 if not holding else -10 ** 9
        best = go(i + 1, left, holding)
        if holding:
            best = max(best, prices[i] - fee + go(i + 1, left, False))
        elif left:
            best = max(best, go(i + 1, left - 1, True) - prices[i])
        return best
    return go(0, k, False)
''', 'the memo fixes the time but not the depth')

CANDIDATES = C
