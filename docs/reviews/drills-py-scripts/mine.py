"""My own solutions to the 30 `py` pack drills, written from the brief alone and by a
method other than the model's. The pandas drills use plain loops (no shift, rolling,
resample, groupby, merge, ffill or pct_change) and only wrap the answer in a Series or frame."""

SOLUTIONS = {}

SOLUTIONS['py-trimmed-fill-mean'] = '''
def trimmed_fill_mean(prices, k):
    s = list(prices)
    if 2 * k >= len(s):
        return None
    for _ in range(k):
        s.remove(min(s))
        s.remove(max(s))
    return sum(s) / len(s)
'''

SOLUTIONS['py-holdings-change'] = '''
def holdings_change(before, after):
    old = dict.fromkeys(before)
    new = dict.fromkeys(after)
    added = [t for t in new if t not in old]
    dropped = [t for t in old if t not in new]
    added.sort()
    dropped.sort()
    kept = 0
    for t in old:
        if t in new:
            kept += 1
    return (added, dropped, kept)
'''

SOLUTIONS['py-format-pence'] = '''
def format_pence(p):
    digits = str(p).lstrip('-')
    while len(digits) < 3:
        digits = '0' + digits
    pounds, pence = digits[:-2], digits[-2:]
    groups = []
    while len(pounds) > 3:
        groups.insert(0, pounds[-3:])
        pounds = pounds[:-3]
    groups.insert(0, pounds)
    return ('-' if p < 0 else '') + chr(163) + ','.join(groups) + '.' + pence
'''

SOLUTIONS['py-cross-up-days'] = '''
def cross_up_days(fast, slow):
    out = []
    was_above = None
    for i in range(len(fast)):
        above = fast[i] > slow[i]
        if i > 0 and above and not was_above:
            out.append(i)
        was_above = above
    return out
'''

SOLUTIONS['py-split-pence'] = '''
from decimal import Decimal

def split_pence(fee, n):
    total = int((Decimal(str(fee)) * 100).to_integral_value())
    base = total // n
    out = [base for _ in range(n)]
    for i in range(total - base * n):
        out[i] += 1
    return out
'''

SOLUTIONS['py-fill-summary'] = '''
import math

def fill_summary(fills):
    groups = {}
    for oid, q, p in fills:
        groups.setdefault(oid, []).append((q, p))
    out = {}
    for oid, pieces in groups.items():
        shares = sum(q for q, _ in pieces)
        out[oid] = (shares, math.fsum(q * p for q, p in pieces) / shares)
    return out
'''

SOLUTIONS['py-quote-ladder'] = '''
def quote_ladder(mid, levels=3, step=0.05, size=100):
    ks = list(range(1, levels + 1))
    bids = [('bid', round(mid - k * step, 2), size * k) for k in ks]
    asks = [('ask', round(mid + k * step, 2), size * k) for k in ks]
    return bids + asks
'''

SOLUTIONS['py-wide-to-long'] = '''
def wide_to_long(text):
    lines = [ln for ln in text.splitlines() if ln.strip() != '']
    if not lines:
        return []
    names = [h.strip() for h in lines[0].split(',')][1:]
    out = []
    for ln in lines[1:]:
        cells = ln.split(',')
        day = cells[0].strip()
        for j, name in enumerate(names):
            cell = cells[j + 1].strip() if j + 1 < len(cells) else ''
            if cell != '':
                out.append((name, day, float(cell)))
    out.sort(key=lambda t: (t[0], t[1]))
    return out
'''

SOLUTIONS['py-batches'] = '''
from itertools import islice

def batches(items, size):
    if size < 1:
        raise ValueError('size')
    it = iter(items)
    while True:
        b = list(islice(it, size))
        if not b:
            return
        yield b
'''

SOLUTIONS['py-split-adjusted'] = '''
def split_adjusted(closes, splits):
    days = sorted(splits)
    out = []
    for i, c in enumerate(closes):
        f = 1.0
        for d in days:
            if d > i:
                f *= splits[d]
        out.append(c / f)
    return out
'''

SOLUTIONS['py-guarded-returns'] = '''
def _read(text):
    if not isinstance(text, str):
        raise TypeError('not text')
    try:
        return float(text)
    except ValueError:
        return None

def guarded_returns(pairs):
    rets, bad, zero = [], 0, 0
    for pair in pairs:
        if not isinstance(pair, (tuple, list)):
            raise TypeError('not a pair')
        o, c = _read(pair[0]), _read(pair[1])
        if o is None or c is None:
            bad += 1
        elif o == 0:
            zero += 1
        else:
            rets.append(c / o - 1)
    return (rets, bad, zero)
'''

SOLUTIONS['py-cost-basis'] = '''
class CostBasis:
    def __init__(self):
        self.qty = 0
        self.cost = 0.0
        self.realised = 0.0

    @property
    def avg_cost(self):
        return self.cost / self.qty if self.qty else 0.0

    def buy(self, qty, price):
        if not qty > 0:
            raise ValueError('qty')
        self.cost += qty * price
        self.qty += qty

    def sell(self, qty, price):
        if not qty > 0 or qty > self.qty:
            raise ValueError('qty')
        avg = self.avg_cost
        self.realised += qty * price - qty * avg
        self.qty -= qty
        self.cost = self.qty * avg

    def unrealised(self, price):
        return self.qty * price - self.cost
'''

SOLUTIONS['py-growth-curve'] = '''
from itertools import accumulate

def growth_curve(rets, start=100.0):
    return list(accumulate(rets, lambda v, r: v + v * r, initial=start))
'''

SOLUTIONS['py-bar-limits'] = '''
def bar_limits(values, pad=0.1):
    top = max([v for v in values if v > 0], default=0.0)
    bottom = min([v for v in values if v < 0], default=0.0)
    span = top - bottom
    if span == 0:
        return (0.0, 1.0)
    return (bottom - pad * span if bottom < 0 else 0.0, top + pad * span if top > 0 else 0.0)
'''

SOLUTIONS['py-bin-counts'] = '''
from bisect import bisect_right

def bin_counts(rets, edges):
    k = len(edges) - 1
    counts = [0] * k
    for x in rets:
        if x < edges[0] or x > edges[k]:
            continue
        i = bisect_right(edges, x) - 1
        counts[min(i, k - 1)] += 1
    return counts
'''

SOLUTIONS['py-paired-returns'] = '''
def paired_returns(a, b):
    out = []
    prev = None
    for d in sorted(a):
        if d not in b:
            continue
        if prev is not None:
            out.append(((a[d] - a[prev]) / a[prev], (b[d] - b[prev]) / b[prev]))
        prev = d
    return out
'''

SOLUTIONS['py-underwater-series'] = '''
def underwater_series(values):
    dd, days = [], []
    at = 0
    for t, v in enumerate(values):
        if v >= values[at]:
            at = t
        dd.append((v - values[at]) / values[at])
        days.append(t - at)
    return (dd, days)
'''

SOLUTIONS['py-month-grid'] = '''
import math

def month_grid(rows):
    cells = {}
    months, tickers = set(), set()
    for date, ticker, r in rows:
        m = date.rsplit('-', 1)[0]
        months.add(m)
        tickers.add(ticker)
        cells.setdefault(m, {}).setdefault(ticker, []).append(1 + r)
    months, tickers = sorted(months), sorted(tickers)
    grid = []
    for m in months:
        row = []
        for t in tickers:
            row.append(math.prod(cells[m][t]) - 1 if t in cells[m] else None)
        grid.append(row)
    return (months, tickers, grid)
'''

SOLUTIONS['py-big-move-days'] = '''
def big_move_days(returns, volumes, move, min_volume):
    out = []
    for i in range(len(returns)):
        r = returns[i]
        if (r >= move or -r >= move) and volumes[i] >= min_volume:
            out.append(i)
    return out
'''

SOLUTIONS['py-best-desk-each-day'] = '''
def best_desk(pnl, desks):
    out = []
    for row in pnl:
        best = 0
        for j in range(1, len(row)):
            if row[j] > row[best]:
                best = j
        out.append(desks[best])
    return out
'''

SOLUTIONS['py-carry-forward-limit'] = '''
import pandas as pd

def carry_forward(close, limit):
    vals = close.tolist()
    out = []
    last, run = None, 0
    for v in vals:
        if v == v:
            last, run = v, 0
            out.append(v)
        else:
            run += 1
            out.append(last if (last is not None and run <= limit) else float('nan'))
    return pd.Series(out, index=close.index, dtype=float)
'''

SOLUTIONS['py-volume-surge'] = '''
import csv

def volume_surges(path):
    with open(path, newline='') as f:
        rows = list(csv.DictReader(f))
    out = []
    for prev, row in zip(rows, rows[1:]):
        if int(row['volume']) >= 2 * int(prev['volume']):
            out.append(row['date'])
    return out
'''

SOLUTIONS['py-fx-to-pounds'] = '''
import numpy as np

def to_pounds(prices, rates):
    out = np.empty((len(prices), len(prices[0])))
    for i, row in enumerate(prices):
        for j, p in enumerate(row):
            out[i, j] = p * rates[i]
    return out
'''

SOLUTIONS['py-day-fills'] = '''
import pandas as pd

def day_fill_summary(fills):
    acc = {}
    for ticker, side, qty, price in zip(fills['ticker'].tolist(), fills['side'].tolist(),
                                        fills['qty'].tolist(), fills['price'].tolist()):
        a = acc.setdefault(ticker, [0, 0.0, 0, 0])
        a[0] += qty if side == 'B' else -qty
        a[1] += qty * price
        a[2] += qty
        a[3] += 1
    names = sorted(acc)
    return pd.DataFrame({'net': [acc[t][0] for t in names],
                         'vwap': [acc[t][1] / acc[t][2] for t in names],
                         'fills': [acc[t][3] for t in names]}, index=names)
'''

SOLUTIONS['py-weekly-range'] = '''
import datetime
import pandas as pd

def weekly_range(close):
    weeks = {}
    for stamp, v in zip(close.index, close.tolist()):
        day = stamp.date()
        friday = day + datetime.timedelta(days=(4 - day.weekday()) % 7)
        weeks.setdefault(friday, []).append(v)
    keys = sorted(weeks)
    vals = [(max(weeks[k]) - min(weeks[k])) / weeks[k][0] for k in keys]
    return pd.Series(vals, index=pd.DatetimeIndex(pd.to_datetime(keys)), dtype=float)
'''

SOLUTIONS['py-gap-aware-returns'] = '''
import pandas as pd

def gap_returns(close):
    vals = close.tolist()
    out = []
    for i, v in enumerate(vals):
        if i == 0 or v != v or vals[i - 1] != vals[i - 1]:
            out.append(float('nan'))
        else:
            out.append(v / vals[i - 1] - 1)
    return pd.Series(out, index=close.index, dtype=float)
'''

SOLUTIONS['py-combined-desk-pnl'] = '''
import pandas as pd

def combined_pnl(a, b):
    total = {}
    for s in (a, b):
        for stamp, v in zip(s.index, s.tolist()):
            total[stamp] = total.get(stamp, 0.0) + v
    keys = sorted(total)
    return pd.Series([total[k] for k in keys], index=pd.DatetimeIndex(keys, name='date'), dtype=float)
'''

SOLUTIONS['py-prior-zscore'] = '''
import statistics
import pandas as pd

def prior_zscore(close, n):
    vals = close.tolist()
    out = []
    for t, c in enumerate(vals):
        if t < n:
            out.append(float('nan'))
            continue
        before = vals[t - n:t]
        s = statistics.stdev(before)
        out.append((c - statistics.fmean(before)) / s if s > 0 else float('nan'))
    return pd.Series(out, index=close.index, dtype=float)
'''

SOLUTIONS['py-excess-vs-benchmark'] = '''
import pandas as pd

def mean_excess_bps(prices, bench):
    b = sorted(zip(bench['date'].tolist(), bench['close'].tolist()))
    bret = {}
    for (d0, c0), (d1, c1) in zip(b, b[1:]):
        bret[d1] = c1 / c0 - 1
    by = {}
    for d, t, c in zip(prices['date'].tolist(), prices['ticker'].tolist(), prices['close'].tolist()):
        by.setdefault(t, []).append((d, c))
    names, vals = [], []
    for t in sorted(by):
        rows = sorted(by[t])
        ex = [c1 / c0 - 1 - bret[d1] for (d0, c0), (d1, c1) in zip(rows, rows[1:]) if d1 in bret]
        if ex:
            names.append(t)
            vals.append(10000 * sum(ex) / len(ex))
    return pd.Series(vals, index=names, dtype=float)
'''

SOLUTIONS['py-month-hit-rate'] = '''
import pandas as pd

def month_hit_rate(close):
    last = {}
    for stamp, v in zip(close.index, close.tolist()):
        last[(stamp.year, stamp.month)] = v      # the index is sorted, so the last write is the month end
    keys = sorted(last)
    ups, n = {}, {}
    for k0, k1 in zip(keys, keys[1:]):
        m = k1[1]
        n[m] = n.get(m, 0) + 1
        ups[m] = ups.get(m, 0) + (1 if last[k1] > last[k0] else 0)
    months = sorted(n)
    return pd.Series([ups[m] / n[m] for m in months], index=months, dtype=float)
'''
