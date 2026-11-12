"""The delta reader's own solutions, written from statement.py output alone (prose, question, starter, two examples),
before the models or the hidden tests were read. One source string per task id."""
MINE = {}

MINE['edge-case-list-second-largest'] = '''
def runner_up_gap(xs):
    d = sorted(set(xs))
    if len(d) < 2:
        return None
    return d[-1] - d[-2]
'''

MINE['ds-pointers-merge-ticks'] = '''
def merge_ticks(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        ta, pa = a[i]
        tb, pb = b[j]
        if ta < tb:
            out.append((ta, pa)); i += 1
        elif tb < ta:
            out.append((tb, pb)); j += 1
        else:
            out.append((ta, (pa + pb) / 2)); i += 1; j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
'''

MINE['pf-collections-top-symbols'] = '''
def busiest_symbols(trades, k):
    total = {}
    for sym, q in trades:
        total[sym] = total.get(sym, 0) + abs(q)
    names = sorted(total, key=lambda s: -total[s])      # stable: ties stay in first-trade order
    return names[:k] if k > 0 else []
'''

MINE['ds-hashing-price-mode'] = '''
def modal_prices(prices):
    count = {}
    for p in prices:
        count[p] = count.get(p, 0) + 1
    if not count:
        return []
    top = max(count.values())
    return sorted((p for p in count if count[p] == top), reverse=True)
'''

MINE['ds-arrays-sign-changes'] = '''
def sign_changes(pnl):
    last = 0
    n = 0
    for x in pnl:
        if x == 0:
            continue
        s = 1 if x > 0 else -1
        if last and s != last:
            n += 1
        last = s
    return n
'''

MINE['pf-idioms-count-above-mean'] = '''
def above_mean(xs):
    if not xs:
        return 0
    s, n = sum(xs), len(xs)
    return sum(1 for x in xs if x * n > s)
'''

MINE['ds-arrays-local-peaks'] = '''
def local_peaks(xs):
    return [i for i in range(1, len(xs) - 1) if xs[i - 1] < xs[i] > xs[i + 1]]
'''

MINE['at-search-smallest-n'] = '''
def rows_needed(target):
    lo, hi = 0, 2 * 10**9
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo
'''

MINE['at-search-count-in-range'] = '''
def count_in_range(xs, lo, hi):
    def first(pred):
        a, b = 0, len(xs)
        while a < b:
            m = (a + b) // 2
            if pred(xs[m]):
                b = m
            else:
                a = m + 1
        return a
    return max(0, first(lambda v: v > hi) - first(lambda v: v >= lo))
'''

MINE['gd-dp-walk-above-zero'] = '''
def nonneg_walk_counts(n):
    cur = {0: 1}
    for _ in range(n):
        nxt = {}
        for pos, c in cur.items():
            nxt[pos + 1] = nxt.get(pos + 1, 0) + c
            if pos > 0:
                nxt[pos - 1] = nxt.get(pos - 1, 0) + c
        cur = nxt
    return cur
'''

MINE['pf-idioms-trend-direction'] = '''
def trend(xs):
    if len(xs) < 2:
        return 0
    if all(b > a for a, b in zip(xs, xs[1:])):
        return 1
    if all(b < a for a, b in zip(xs, xs[1:])):
        return -1
    return 0
'''

MINE['edge-case-list-to-pence'] = '''
def to_pence(text):
    s = text.strip()
    neg = s.startswith('-')
    if neg:
        s = s[1:].strip()
    s = s.replace('£', '').replace(',', '').strip()
    if '.' in s:
        whole, frac = s.split('.')
    else:
        whole, frac = s, ''
    frac = (frac + '00')[:2]
    pence = int(whole or '0') * 100 + int(frac)
    return -pence if neg else pence
'''

MINE['at-greedy-orders-to-fill'] = '''
def orders_to_fill(sizes, target):
    if target <= 0:
        return 0
    total = 0
    for n, s in enumerate(sorted(sizes, reverse=True), 1):
        total += s
        if total >= target:
            return n
    return -1
'''

MINE['pf-functions-binom-tail'] = '''
from fractions import Fraction
import math

def binom_tail(n, k):
    if k <= 0:
        return Fraction(1)
    if k > n:
        return Fraction(0)
    return Fraction(sum(math.comb(n, j) for j in range(k, n + 1)), 2 ** n)
'''
