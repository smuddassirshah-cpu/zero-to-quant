"""Pure-Python reference values (method A) read straight from the CSV files."""
import csv, math, bisect, random
D = '/home/user/zero-to-quant/.claude/worktrees/agent-a8859a2b6006bfb36/app/content/data/'


def rd(name):
    return list(csv.DictReader(open(D + name, newline='')))


# ---- ticks ----
def ticks_clean():
    by = {}
    for r in rd('ticks-gaps.csv'):
        if r['price'].strip() == '':
            continue
        by.setdefault(int(r['t_sec']), []).append(float(r['price']))
    ts = sorted(by)
    return ts, [sum(by[t]) / len(by[t]) for t in ts]


TS, PS = ticks_clean()


def price_at(t):
    if t <= TS[0]: return PS[0]
    if t >= TS[-1]: return PS[-1]
    j = bisect.bisect_right(TS, t)
    if TS[j - 1] == t: return PS[j - 1]
    return PS[j - 1] + (PS[j] - PS[j - 1]) * (t - TS[j - 1]) / (TS[j] - TS[j - 1])


# ---- towns ----
def towns():
    by = {}
    for r in rd('towns-temp.csv'):
        by.setdefault(r['town'], []).append((int(r['day']), float(r['temp_c'])))
    return by


def line_stats(pts):
    n = len(pts)
    if n < 3: return None
    mx = sum(a for a, _ in pts) / n; my = sum(b for _, b in pts) / n
    sxx = sum((a - mx) ** 2 for a, _ in pts); syy = sum((b - my) ** 2 for _, b in pts); sxy = sum((a - mx) * (b - my) for a, b in pts)
    m = sxy / sxx
    return {"slope": m, "intercept": my - m * mx, "r2": sxy * sxy / (sxx * syy), "n": n}


TOWNS = {t: line_stats(p) for t, p in towns().items()}


# ---- orders ----
def orders_clean():
    seen = set(); out = []
    for r in rd('orders-messy.csv'):
        oid = int(r['order_id'])
        if oid in seen: continue
        seen.add(oid)
        if r['price'].strip() == '': continue
        p = float(r['price'])
        if p <= 0: continue
        out.append({"id": oid, "symbol": r['symbol'].strip().upper(), "side": r['side'].strip().upper(), "qty": int(r['qty'].replace(',', '')), "price": p, "mid": float(r['mid'])})
    return out


ORD = orders_clean()


def vwap(sym):
    rows = [r for r in ORD if r['symbol'] == sym]
    return sum(r['price'] * r['qty'] for r in rows) / sum(r['qty'] for r in rows)


def slip_fit():
    xs = []; ys = []
    for r in ORD:
        sd = 1 if r['side'] == 'B' else -1
        ys.append(sd * (r['price'] - r['mid']) / r['mid'] * 1e4); xs.append(math.log(r['qty'] / 100))
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs); sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys)); syy = sum((y - my) ** 2 for y in ys)
    m = sxy / sxx; b = my - m * mx
    sse = sum((y - b - m * x) ** 2 for x, y in zip(xs, ys))
    se = math.sqrt(sse / (n - 2) / sxx)
    return {"slope": m, "intercept": b, "r2": sxy * sxy / (sxx * syy), "mean": my, "se": se, "n": n}


SLIP = slip_fit()

# ---- houses ----
def houses():
    rows = rd('houses.csv')
    return [float(r['price_k']) for r in rows if float(r['price_k']) <= 5000]


if __name__ == '__main__':
    print(len(TS), TS[0], TS[-1], PS[0], PS[-1])
    for t in (12000, 100, 23000, 3333, 16000, 20000):
        print(t, repr(price_at(t)))
    print({k: (round(v['slope'], 7) if v else None) for k, v in TOWNS.items()})
    print(len(ORD), {s: (sum(1 for r in ORD if r['symbol'] == s), round(vwap(s), 4)) for s in ('ALPHA', 'BRAVO', 'CHARLIE')}, sum(r['qty'] for r in ORD))
    print(SLIP)
    h = houses(); print(len(h), sum(h) / len(h))
    print('B count', sum(1 for r in ORD if r['side'] == 'B'), 'notional', sum(r['price'] * r['qty'] for r in ORD))
