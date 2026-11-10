"""Wrong (or brief-breaking) solutions the authors did not plant, at least one a drill.
Each entry: (drill id, label, source). `harness.py wrong` reports which pass every hidden test."""

C = []


def add(drill, label, src):
    C.append((drill, label, src))


add('py-trimmed-fill-mean', 'no sort: slices the list as given', '''
def trimmed_fill_mean(prices, k):
    kept = prices[k:len(prices) - k]
    if not kept:
        return None
    return sum(kept) / len(kept)
''')
add('py-trimmed-fill-mean', 'too few prices: plain mean, not None', '''
def trimmed_fill_mean(prices, k):
    s = sorted(prices)
    if not s:
        return None
    if 2 * k >= len(s):
        return sum(s) / len(s)
    s = s[k:len(s) - k]
    return sum(s) / len(s)
''')

add('py-holdings-change', 'kept counts repeats in `before`', '''
def holdings_change(before, after):
    old, new = set(before), set(after)
    return (sorted(new - old), sorted(old - new), len([t for t in before if t in new]))
''')
add('py-holdings-change', 'tickers compared without case', '''
def holdings_change(before, after):
    old = {t.upper() for t in before}
    new = {t.upper() for t in after}
    return (sorted(new - old), sorted(old - new), len(old & new))
''')

add('py-format-pence', 'pence not padded to two digits', '''
def format_pence(p):
    sign = '-' if p < 0 else ''
    return f'{sign}£{abs(p) // 100:,}.{abs(p) % 100}'
''')
add('py-format-pence', 'sign read from the pounds, lost under £1', '''
def format_pence(p):
    pounds = int(p / 100) if abs(p) < 10 ** 15 else (abs(p) // 100) * (1 if p > 0 else -1)
    sign = '-' if pounds < 0 else ''
    return f'{sign}£{abs(p) // 100:,}.{abs(p) % 100:02d}'
''')

add('py-cross-up-days', "yesterday's fast against today's slow", '''
def cross_up_days(fast, slow):
    return [i for i in range(1, len(fast)) if fast[i - 1] <= slow[i] and fast[i] > slow[i]]
''')
add('py-cross-up-days', "today's fast against yesterday's slow", '''
def cross_up_days(fast, slow):
    return [i for i in range(1, len(fast)) if fast[i - 1] <= slow[i - 1] and fast[i] > slow[i - 1]]
''')
add('py-cross-up-days', 'at or above counts as above today', '''
def cross_up_days(fast, slow):
    return [i for i in range(1, len(fast)) if fast[i - 1] <= slow[i - 1] and fast[i] >= slow[i]]
''')

add('py-split-pence', 'math.ceil(fee * 100)', '''
import math

def split_pence(fee, n):
    total = math.ceil(fee * 100)
    share, spare = divmod(total, n)
    return [share + 1] * spare + [share] * (n - spare)
''')
add('py-split-pence', 'digits of str(fee) joined', '''
def split_pence(fee, n):
    total = int(str(fee).replace('.', ''))
    share, spare = divmod(total, n)
    return [share + 1] * spare + [share] * (n - spare)
''')

add('py-fill-summary', 'average rounded to 4 places', '''
def fill_summary(fills):
    qty, spent = {}, {}
    for oid, q, p in fills:
        qty[oid] = qty.get(oid, 0) + q
        spent[oid] = spent.get(oid, 0.0) + q * p
    return {o: (qty[o], round(spent[o] / qty[o], 4)) for o in qty}
''')
add('py-fill-summary', 'only neighbouring fills of an order are joined', '''
from itertools import groupby

def fill_summary(fills):
    out = {}
    for oid, grp in groupby(fills, key=lambda f: f[0]):
        grp = list(grp)
        q = sum(g[1] for g in grp)
        out[oid] = (q, sum(g[1] * g[2] for g in grp) / q)
    return out
''')

add('py-quote-ladder', 'size doubles at each level', '''
def quote_ladder(mid, levels=3, step=0.05, size=100):
    out = [('bid', round(mid - k * step, 2), size * 2 ** (k - 1)) for k in range(1, levels + 1)]
    return out + [('ask', round(mid + k * step, 2), size * 2 ** (k - 1)) for k in range(1, levels + 1)]
''')
add('py-quote-ladder', 'bids and asks interleaved by level', '''
def quote_ladder(mid, levels=3, step=0.05, size=100):
    out = []
    for k in range(1, levels + 1):
        out.append(('bid', round(mid - k * step, 2), k * size))
        out.append(('ask', round(mid + k * step, 2), k * size))
    return out
''')

add('py-wide-to-long', 'sorted by ticker only (file order of dates kept)', '''
import csv, io

def wide_to_long(text):
    rows = [r for r in csv.reader(io.StringIO(text)) if r]
    if not rows:
        return []
    names = [h.strip() for h in rows[0][1:]]
    out = []
    for row in rows[1:]:
        for name, cell in zip(names, row[1:]):
            if cell.strip():
                out.append((name, row[0].strip(), float(cell)))
    return sorted(out, key=lambda t: t[0])
''')
add('py-wide-to-long', 'a close of 0 read as no close', '''
import csv, io

def wide_to_long(text):
    rows = [r for r in csv.reader(io.StringIO(text)) if r]
    if not rows:
        return []
    names = [h.strip() for h in rows[0][1:]]
    out = []
    for row in rows[1:]:
        for name, cell in zip(names, row[1:]):
            if cell.strip() and float(cell):
                out.append((name, row[0].strip(), float(cell)))
    return sorted(out)
''')

add('py-batches', 'reads one item ahead before handing a batch on', '''
def batches(items, size):
    if size < 1:
        raise ValueError('size')
    batch = []
    for item in items:
        if len(batch) == size:
            yield batch
            batch = []
        batch.append(item)
    if batch:
        yield batch
''')

add('py-split-adjusted', "uses up the caller's dict of splits", '''
def split_adjusted(closes, splits):
    out = []
    factor = 1.0
    for i in range(len(closes) - 1, -1, -1):
        out.append(closes[i] / factor)
        if i in splits:
            factor *= splits.pop(i)
    return out[::-1]
''')
add('py-split-adjusted', 'only the latest split applied', '''
def split_adjusted(closes, splits):
    if not splits:
        return list(closes)
    d = max(splits)
    return [c / splits[d] if i < d else c for i, c in enumerate(closes)]
''')

add('py-guarded-returns', "strips thousands commas before reading ('1,200.00' is a number)", '''
def guarded_returns(pairs):
    rets, bad, zero = [], 0, 0
    for o_text, c_text in pairs:
        try:
            o = float(o_text.replace(',', ''))
            c = float(c_text.replace(',', ''))
        except ValueError:
            bad += 1
            continue
        except AttributeError:
            raise TypeError('not text')
        if o == 0:
            zero += 1
        else:
            rets.append(c / o - 1)
    return (rets, bad, zero)
''')
add('py-guarded-returns', 'zero open judged before the close is read', '''
def guarded_returns(pairs):
    rets, bad, zero = [], 0, 0
    for o_text, c_text in pairs:
        try:
            o = float(o_text)
            if o == 0:
                zero += 1
                continue
            c = float(c_text)
        except ValueError:
            bad += 1
            continue
        rets.append(c / o - 1)
    return (rets, bad, zero)
''')

COST = '''
class CostBasis:
    def __init__(self):
        self.qty = 0
        self.avg_cost = 0.0
        self.realised = 0.0

    def buy(self, qty, price):
        %s

    def sell(self, qty, price):
        if qty <= 0 or qty > self.qty:
            raise ValueError('qty')
        self.realised = self.realised + qty * (price - self.avg_cost)
        self.qty = self.qty - qty
        if self.qty == 0:
            self.avg_cost = 0.0

    def unrealised(self, price):
        return self.qty * (price - self.avg_cost)
'''
add('py-cost-basis', 'buy refuses 0 only: a negative buy goes through', COST % '''if qty == 0:
            raise ValueError('qty')
        cost = self.qty * self.avg_cost + qty * price
        self.qty = self.qty + qty
        self.avg_cost = cost / self.qty''')
add('py-cost-basis', 'buy changes the position, then checks', COST % '''cost = self.qty * self.avg_cost + qty * price
        self.qty = self.qty + qty
        if qty <= 0:
            raise ValueError('qty')
        self.avg_cost = cost / self.qty''')

add('py-growth-curve', 'each day grows from the start, not from the day before', '''
def growth_curve(rets, start=100.0):
    return [start] + [start * (1 + r) for r in rets]
''')
add('py-growth-curve', 'values rounded to pence', '''
def growth_curve(rets, start=100.0):
    out = [start]
    for r in rets:
        out.append(out[-1] * (1 + r))
    return [round(v, 2) for v in out]
''')

add('py-bar-limits', 'span taken from the data, not from zero', '''
def bar_limits(values, pad=0.1):
    if not values or max(values) == min(values) == 0:
        return (0.0, 1.0)
    span = max(values) - min(values)
    lo, hi = min(0.0, min(values)), max(0.0, max(values))
    return (lo - pad * span if lo < 0 else lo, hi + pad * span if hi > 0 else hi)
''')
add('py-bar-limits', 'pads the zero end as well', '''
def bar_limits(values, pad=0.1):
    lo, hi = min([0.0] + list(values)), max([0.0] + list(values))
    span = hi - lo
    if span == 0:
        return (0.0, 1.0)
    return (lo - pad * span, hi + pad * span)
''')

add('py-bin-counts', 'bins assumed equal in width', '''
def bin_counts(rets, edges):
    k = len(edges) - 1
    width = (edges[-1] - edges[0]) / k
    counts = [0] * k
    for x in rets:
        if x < edges[0] or x > edges[-1]:
            continue
        counts[min(int((x - edges[0]) / width), k - 1)] += 1
    return counts
''')
add('py-bin-counts', 'first bin that touches the value wins', '''
def bin_counts(rets, edges):
    k = len(edges) - 1
    counts = [0] * k
    for x in rets:
        for i in range(k):
            if edges[i] <= x <= edges[i + 1]:
                counts[i] += 1
                break
    return counts
''')

add('py-paired-returns', "each return from the share's own previous date", '''
def paired_returns(a, b):
    da, db = sorted(a), sorted(b)
    out = []
    shared = [d for d in da if d in b]
    for d in shared[1:]:
        pa, pb = da[da.index(d) - 1], db[db.index(d) - 1]
        out.append((a[d] / a[pa] - 1, b[d] / b[pb] - 1))
    return out
''')

add('py-underwater-series', 'peak of the whole series, not the running peak', '''
def underwater_series(values):
    if not values:
        return ([], [])
    peak = max(values)
    at = values.index(peak)
    dd, days, count = [], [], 0
    run = None
    for v in values:
        if run is None or v >= run:
            run, count = v, 0
        else:
            count += 1
        dd.append(v / peak - 1)
        days.append(count)
    return (dd, days)
''')
add('py-underwater-series', 'count never resets after the first fall', '''
def underwater_series(values):
    dd, days, peak, count = [], [], None, 0
    for v in values:
        if peak is None or v >= peak:
            peak = v
        if v < peak:
            count += 1
        dd.append(v / peak - 1)
        days.append(count if v < peak else 0)
    return (dd, days)
''')

add('py-month-grid', 'a month that loses everything shows None', '''
def month_grid(rows):
    growth = {}
    for date, ticker, r in rows:
        key = (date[:7], ticker)
        growth[key] = growth.get(key, 1.0) * (1 + r)
    months = sorted({m for m, _ in growth})
    tickers = sorted({t for _, t in growth})
    grid = [[growth[(m, t)] - 1 if growth.get((m, t)) else None for t in tickers] for m in months]
    return (months, tickers, grid)
''')
add('py-month-grid', 'tickers in first-seen order', '''
def month_grid(rows):
    growth = {}
    for date, ticker, r in rows:
        key = (date[:7], ticker)
        growth[key] = growth.get(key, 1.0) * (1 + r)
    months = sorted({m for m, _ in growth})
    tickers = list(dict.fromkeys(t for _, t in growth))
    grid = [[growth[(m, t)] - 1 if (m, t) in growth else None for t in tickers] for m in months]
    return (months, tickers, grid)
''')

add('py-big-move-days', 'volume must be strictly above the minimum', '''
import numpy as np

def big_move_days(returns, volumes, move, min_volume):
    r, v = np.asarray(returns, dtype=float), np.asarray(volumes, dtype=float)
    return np.flatnonzero((np.abs(r) >= move) & (v > min_volume)).tolist()
''')

add('py-best-desk-each-day', 'looks the best value up in a dict: last desk wins a tie', '''
def best_desk(pnl, desks):
    return [dict(zip(row, desks))[max(row)] for row in pnl]
''')

add('py-carry-forward-limit', 'fills a gap only when the whole gap is short', '''
import pandas as pd

def carry_forward(close, limit):
    out = close.copy()
    vals = close.tolist()
    i, n = 0, len(vals)
    while i < n:
        if vals[i] != vals[i]:
            j = i
            while j < n and vals[j] != vals[j]:
                j += 1
            if i > 0 and j - i <= limit:
                out.iloc[i:j] = vals[i - 1]
            i = j
        else:
            i += 1
    return out
''')
add('py-carry-forward-limit', 'limit 0 turned into no limit', '''
import pandas as pd

def carry_forward(close, limit):
    return close.ffill(limit=limit or None)
''')

add('py-volume-surge', 'ratio rounded before the comparison', '''
import pandas as pd

def volume_surges(path):
    df = pd.read_csv(path, index_col="date", parse_dates=True)
    v = df["volume"]
    surge = (v / v.shift(1)).round() >= 2
    return [d.strftime("%Y-%m-%d") for d in df.index[surge]]
''')

add('py-fx-to-pounds', 'rounded to pence', '''
import numpy as np

def to_pounds(prices, rates):
    p, r = np.asarray(prices, dtype=float), np.asarray(rates, dtype=float)
    return np.round(p * r[:, None], 2)
''')

add('py-day-fills', 'vwap over the buys only', '''
import numpy as np
import pandas as pd

def day_fill_summary(fills):
    df = fills.copy()
    df["signed"] = np.where(df["side"] == "B", df["qty"], -df["qty"])
    df["bq"] = np.where(df["side"] == "B", df["qty"], 0)
    df["bv"] = df["bq"] * df["price"]
    g = df.groupby("ticker").agg(net=("signed", "sum"), bv=("bv", "sum"), bq=("bq", "sum"), fills=("qty", "size"))
    g["vwap"] = g["bv"] / g["bq"]
    return g[["net", "vwap", "fills"]]
''')
add('py-day-fills', 'fills counts different sizes, not rows', '''
import numpy as np
import pandas as pd

def day_fill_summary(fills):
    df = fills.copy()
    df["signed"] = np.where(df["side"] == "B", df["qty"], -df["qty"])
    df["value"] = df["qty"] * df["price"]
    g = df.groupby("ticker").agg(net=("signed", "sum"), value=("value", "sum"), qty=("qty", "sum"), fills=("qty", "nunique"))
    g["vwap"] = g["value"] / g["qty"]
    return g[["net", "vwap", "fills"]]
''')

add('py-weekly-range', 'weeks run Monday to Sunday (a Saturday close joins the week before)', '''
import datetime
import pandas as pd

def weekly_range(close):
    weeks = {}
    for stamp, v in zip(close.index, close.tolist()):
        day = stamp.date()
        friday = day - datetime.timedelta(days=day.weekday()) + datetime.timedelta(days=4)
        weeks.setdefault(friday, []).append(v)
    keys = sorted(weeks)
    return pd.Series([(max(weeks[k]) - min(weeks[k])) / weeks[k][0] for k in keys],
                     index=pd.DatetimeIndex(pd.to_datetime(keys)), dtype=float)
''')
add('py-weekly-range', "divides by the week's low", '''
import pandas as pd

def weekly_range(close):
    w = close.resample("W-FRI")
    return ((w.max() - w.min()) / w.min()).dropna()
''')

add('py-gap-aware-returns', 'masks only the day after a gap', '''
import pandas as pd

def gap_returns(close):
    return close.pct_change().where(close.shift(1).notna())
''')

add('py-combined-desk-pnl', 'combine_first: desk a wins a shared day', '''
import pandas as pd

def combined_pnl(a, b):
    return a.combine_first(b).sort_index()
''')
add('py-combined-desk-pnl', 'adds, then fills the gaps with 0', '''
import pandas as pd

def combined_pnl(a, b):
    return (a + b).fillna(0)
''')

add('py-prior-zscore', 'mean ends yesterday, deviation ends today', '''
import pandas as pd

def prior_zscore(close, n):
    m = close.rolling(n).mean().shift(1)
    s = close.rolling(n).std()
    z = (close - m) / s
    return z.where((s > 0) & m.notna())
''')
add('py-prior-zscore', 'window of n + 1 that drops nothing', '''
import pandas as pd

def prior_zscore(close, n):
    w = close.shift(1).rolling(n + 1, min_periods=n)
    s = w.std()
    return ((close - w.mean()) / s).where(s > 0)
''')

add('py-excess-vs-benchmark', "index return taken over the share's own dates", '''
import pandas as pd

def mean_excess_bps(prices, bench):
    out = {}
    b = bench.rename(columns={"close": "bench"})
    for t, g in prices.groupby("ticker"):
        m = pd.merge(g, b, on="date").sort_values("date")
        ex = (m["close"].pct_change() - m["bench"].pct_change()).dropna()
        if len(ex):
            out[t] = ex.mean() * 10000
    return pd.Series(out, dtype=float).sort_index()
''')
add('py-excess-vs-benchmark', 'mean share return less the mean index return of all dates', '''
import pandas as pd

def mean_excess_bps(prices, bench):
    p = prices.sort_values("date").copy()
    p["ret"] = p.groupby("ticker")["close"].pct_change()
    b = bench.sort_values("date")["close"].pct_change().mean()
    r = p.dropna(subset=["ret"]).groupby("ticker")["ret"].mean()
    return (r - b) * 10000
''')

add('py-month-hit-rate', 'monthly mean close, not the last close', '''
import pandas as pd

def month_hit_rate(close):
    ret = close.resample("ME").mean().pct_change().dropna()
    return (ret > 0).groupby(ret.index.month).mean()
''')
add('py-month-hit-rate', 'every calendar month listed, 0.0 where none', '''
import pandas as pd

def month_hit_rate(close):
    ret = close.resample("ME").last().pct_change().dropna()
    return (ret > 0).groupby(ret.index.month).mean().reindex(range(1, 13)).fillna(0.0)
''')

CANDIDATES = C

# --- Not wrong: solutions that keep to the brief and are still failed (findings 1 and 9) ---
add('py-paired-returns', 'RIGHT by the brief: sorts the dates as dates', '''
from datetime import date

def paired_returns(a, b):
    days = sorted((d for d in a if d in b), key=date.fromisoformat)
    return [(a[y] / a[x] - 1, b[y] / b[x] - 1) for x, y in zip(days, days[1:])]
''')
add('py-wide-to-long', 'RIGHT: csv.reader over text.splitlines(), as lesson l10 reads text', '''
import csv

def wide_to_long(text):
    rows = [r for r in csv.reader(text.splitlines()) if r]
    if not rows:
        return []
    names = [h.strip() for h in rows[0][1:]]
    out = []
    for row in rows[1:]:
        for name, cell in zip(names, row[1:]):
            if cell.strip():
                out.append((name, row[0].strip(), float(cell)))
    return sorted(out)
''')
add('py-guarded-returns', "the text 'nan' read as a number (the model does this)", '''
def guarded_returns(pairs):
    rets, bad, zero = [], 0, 0
    for o_text, c_text in pairs:
        try:
            o, c = float(o_text), float(c_text)
        except ValueError:
            bad += 1
            continue
        if o == 0:
            zero += 1
        else:
            rets.append(c / o - 1)
    return (rets, bad, zero)
''')
