"""numpy-pandas L2 h-fills-report and L3 h-trend-shares (code: shipped, starter, reader solutions, planted slips,
rounding and tie margins). Run with the venv Python (NumPy 2.5.4), a NumPy 2.0.2 venv, and Pyodide via pyo11.mjs."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fractions import Fraction as F
import numpy as np, pandas as pd
from harness11 import item, summary, patched

bad = 0
def check(name, ok):
    global bad
    print(("ok   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1
print("numpy", np.__version__, "pandas", pd.__version__, sys.platform)

# ---------- L2
it = item("numpy-pandas", "homework-2.json", "h-fills-report")
w = it["widget"]; sol = w["solution"]
print("L2 h-fills-report")
f, _ = summary(w, sol, "shipped solution", "all"); check("L2 shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("L2 starter fails", len(f) > 0)
mine = r'''
import pandas as pd
def fills_report(ids, ticker, side, qty, price, a, b):
    sq = [q if s == "buy" else -q for s, q in zip(side, qty)]
    px = pd.Series([float("nan") if p is None else p for p in price], index=ids, dtype=float)
    fills = pd.DataFrame({"ticker": ticker, "qty": sq}, index=ids)
    fills["value"] = fills["qty"] * px
    i, j = list(ids).index(a), list(ids).index(b)
    span = fills["value"].iloc[i:j + 1]
    last = fills["value"].last_valid_index()
    return {"fills": fills, "span": span, "last": last, "net": float(fills["value"].sum())}
'''
f, _ = summary(w, mine, "reader solution (positions from the id list)", "all"); check("L2 reader solution passes", f == [])
L2plants = [
    ("iloc slice by the ids", [('span = fills.loc[a:b, "value"]', 'span = fills["value"].iloc[a:b]')]),
    ("end left out (positions of a and b)", [('span = fills.loc[a:b, "value"]', 'span = fills["value"].iloc[list(ids).index(a):list(ids).index(b)]')]),
    ("chained assignment for the sign", [('fills.loc[fills["side"] == "sell", "qty"] *= -1', 'fills[fills["side"] == "sell"]["qty"] *= -1')]),
    ("index sorted by id", [('index=ids)', 'index=ids).sort_index()')]),
    ("missing price filled with 0", [('fills["value"] = fills["qty"] * fills["price"]', 'fills["value"] = fills["qty"] * fills["price"].fillna(0)')]),
    ("last fill, not last confirmed", [('"last": confirmed.index[-1]', '"last": fills.index[-1]')]),
    ("last = highest confirmed id", [('"last": confirmed.index[-1]', '"last": confirmed.index.max()')]),
    ("net through NumPy, NaN kept", [('"net": float(confirmed.sum())', '"net": float(np.sum(fills["value"].to_numpy()))')]),
    ("qty list signed in place", [('    fills = pd.DataFrame(', '    for i, s in enumerate(side):\n        if s == "sell":\n            qty[i] = -qty[i]\n    fills = pd.DataFrame('),
                                   ('fills.loc[fills["side"] == "sell", "qty"] *= -1', 'pass')]),
    ("span sliced on the id-sorted frame", [('span = fills.loc[a:b, "value"]', 'span = fills.sort_index().loc[a:b, "value"]')]),
    ("unsigned value", [('fills["value"] = fills["qty"] * fills["price"]', 'fills["value"] = fills["qty"].abs() * fills["price"]')]),
]
for name, pairs in L2plants:
    src = patched(sol, *pairs)
    if "np." in src and "import numpy" not in src:
        src = "import numpy as np\n" + src
    f, _ = summary(w, src, "plant: " + name)
    check("L2 plant caught: " + name, len(f) > 0)
# expects by a second route: plain Python on day() and book()
ns = {}; exec(w["prelude"], ns)
ids, tk, sd, qt, px = ns["day"]()
val = [(-q if s == "sell" else q) * p if p is not None else None for s, q, p in zip(sd, qt, px)]
check("day values 2100 1750 -860 1650 NaN 615 NaN", [None if v is None else round(v, 6) for v in val] == [2100.0, 1750.0, -860.0, 1650.0, None, 615.0, None])
check("day net 5255", round(sum(v for v in val if v is not None), 6) == 5255.0)
for seed, want in ((7, (9, -58460.7, 24, 18, 35)), (5, (25, 12943.7, 24, 6))):
    ids, tk, sd, qt, px = ns["book"](seed, 40)
    v = [(-q if s == "sell" else q) * p if p is not None else None for s, q, p in zip(sd, qt, px)]
    last = [i for i, x in zip(ids, v) if x is not None][-1]
    net = sum(x for x in v if x is not None)
    netF = sum(F(-q if s == "sell" else q) * F(str(p)) for s, q, p in zip(sd, qt, px) if p is not None)
    i, j = ids.index(ids[6]), ids.index(ids[29])
    span = list(zip(ids, v))[i:j + 1]
    got = (last, round(net, 2), len(span), span[0][0], span[-1][0]) if seed == 7 else (last, round(net, 2), len(span), sum(x is None for _, x in span))
    check(f"book({seed}, 40) by plain Python: {want}", got == want)
    check(f"book({seed}, 40) exact net {float(netF)} rounds the same and is far from a half-penny", round(float(netF), 2) == want[1] and abs(netF * 100 - round(netF * 100)) < F(1, 4))
    if seed == 5:
        check("book(5, 40): 12 unconfirmed", sum(p is None for p in px) == 12)

# ---------- L3
it = item("numpy-pandas", "homework-3.json", "h-trend-shares")
w = it["widget"]; sol = w["solution"]
print("L3 h-trend-shares")
f, _ = summary(w, sol, "shipped solution", "all"); check("L3 shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("L3 starter fails", len(f) > 0)
mine = r'''
import pandas as pd
def trend_returns(df, fast, slow):
    out = pd.Series(float("nan"), index=df.index)
    for t in df["ticker"].unique():
        rows = df[df["ticker"] == t].sort_values("date")
        c = rows["close"].tolist()
        held = 0
        for k, idx in enumerate(rows.index):
            if k > 0:
                out[idx] = held * (c[k] / c[k - 1] - 1)
            if k + 1 >= slow:
                fa = sum(c[k + 1 - fast:k + 1]) / fast
                sl = sum(c[k + 1 - slow:k + 1]) / slow
                held = 1 if fa > sl else 0
            else:
                held = 0
    return out
'''
f, _ = summary(w, mine, "reader solution (loops per share, sums / window)", "all"); check("L3 reader solution passes", f == [])
np_route = r'''
import numpy as np
import pandas as pd
def trend_returns(df, fast, slow):
    s = df.sort_values(["ticker", "date"])
    out = pd.Series(np.nan, index=df.index)
    for t, g in s.groupby("ticker", sort=False):
        c = g["close"].to_numpy(float)
        cs = np.concatenate([[0.0], np.cumsum(c)])
        k = np.arange(len(c))
        fa = np.where(k + 1 >= fast, (cs[k + 1] - cs[np.maximum(k + 1 - fast, 0)]) / fast, np.nan)
        sl = np.where(k + 1 >= slow, (cs[k + 1] - cs[np.maximum(k + 1 - slow, 0)]) / slow, np.nan)
        pos = (fa > sl).astype(float)
        r = np.full(len(c), np.nan)
        r[1:] = pos[:-1] * (c[1:] / c[:-1] - 1)
        out.loc[g.index] = r
    return out
'''
f, _ = summary(w, np_route, "NumPy cumsum route (means from running sums)", "all")
check("L3 NumPy cumsum route passes (or fails only where float ties break)", f == [])
L3plants = [
    ("no groupby: windows across shares", [('    g = s.groupby("ticker")["close"]', '    g = s.groupby(pd.Series(0, index=s.index))["close"]')]),
    ("no date sort", [('s = df.sort_values("date")', 's = df')]),
    ("position not shifted (look-ahead)", [('held = pos.groupby(s["ticker"]).shift(1)', 'held = pos')]),
    ("future return", [('ret = g.pct_change()', 'ret = g.pct_change().groupby(s["ticker"]).shift(-1)')]),
    (">= instead of >", [('pos = (f > w).astype(int)', 'pos = (f >= w).astype(int)')]),
    ("fast and slow swapped", [('c.rolling(fast).mean())\n', 'c.rolling(slow).mean())\n'), ('c.rolling(slow).mean())       #', 'c.rolling(fast).mean())       #')]),
    ("log returns", [('ret = g.pct_change()', 'ret = g.transform(lambda c: np.log(c).diff())')]),
    ("min_periods=1 (held before the window is full)", [('c.rolling(slow).mean()', 'c.rolling(slow, min_periods=1).mean()'), ('c.rolling(fast).mean()', 'c.rolling(fast, min_periods=1).mean()')]),
    ("shift not grouped", [('held = pos.groupby(s["ticker"]).shift(1)', 'held = pos.shift(1)')]),
    ("df sorted in place", [('s = df.sort_values("date")', 'df.sort_values("date", inplace=True); s = df')]),
    ("result in sorted order, not df's", [('return (held * ret).reindex(df.index)', 'return (held * ret).reset_index(drop=True)')]),
    ("short when fast below slow", [('pos = (f > w).astype(int)', 'pos = (f > w).astype(int) - (f < w).astype(int)')]),
]
for name, pairs in L3plants:
    src = patched(sol, *pairs)
    if "np." in src and "import numpy" not in src:
        src = "import numpy as np\n" + src
    f, _ = summary(w, src, "plant: " + name)
    check("L3 plant caught: " + name, len(f) > 0)
# exact second route on toy and panels: Fractions of the closes, so ties and rounding are exact
ns = {}; exec(w["prelude"], ns)
def exact(df, fast, slow):
    out = {}
    for t in df["ticker"].unique():
        rows = df[df["ticker"] == t].sort_values("date")
        c = [F(str(v)) for v in rows["close"]]
        held, gaps = 0, []
        for k, idx in enumerate(rows.index):
            out[idx] = None if k == 0 else held * (c[k] / c[k - 1] - 1)
            if k + 1 >= slow:
                d = sum(c[k + 1 - fast:k + 1]) / fast - sum(c[k + 1 - slow:k + 1]) / slow
                gaps.append(abs(d))
                held = 1 if d > 0 else 0
            else:
                held = 0
        out.setdefault("_gaps", []).extend(gaps)
    return out
def r6_margin(vals):
    """smallest distance (in units of 1e-6) of any exact value from a rounding boundary at 6 places"""
    m = 1.0
    for v in vals:
        if v is None:
            continue
        x = v * 10 ** 6
        m = min(m, float(abs(x - (x.numerator // x.denominator) - F(1, 2))))
    return m
toy = ns["toy"]()
for fast, slow, t, want in ((2, 4, "KTX", [None, 0.0, 0.0, 0.0, -0.023256, 0.0, 0.0, 0.04878, 0.0]), (2, 4, "LMN", [None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.0125]),
                            (3, 5, "KTX", [None, 0.0, 0.0, 0.0, 0.0, 0.071429, -0.088889, 0.0, 0.069767])):
    e = exact(toy, fast, slow)
    rows = toy[toy["ticker"] == t].sort_values("date").index
    vals = [e[i] for i in rows]
    check(f"toy {t} ({fast}, {slow}) exact route matches the expect", [None if v is None else round(float(v), 6) for v in vals] == want)
    print(f"    rounding margin {r6_margin(vals):.3f} e-6; exact ties in the averages: {sum(g == 0 for g in e['_gaps'])}")
e = exact(toy, 2, 4)
check("toy KTX (2, 4) has an exact tie on 6 Sep (42.5 against 42.5), resolved as out", 0 in e["_gaps"])
for seed, fast, slow in ((4, 5, 20), (2, 3, 10)):
    df = ns["panel"](seed)
    e = exact(df, fast, slow)
    vals = [e[i] for i in df.index]
    gaps = [g for g in e["_gaps"]]
    s = sum(v for v in vals if v is not None)
    print(f"  panel({seed}) ({fast}, {slow}): rows {len(df)}, returns {sum(v is not None for v in vals)}, non-zero {sum(v not in (None, 0) for v in vals)}, "
          f"sum {float(s):.9f}, smallest |fast - slow| {float(min(gaps)):.2e}")
    if seed == 4:
        check("panel(4): (269, 86, -0.065066) by the exact route", (sum(v is not None for v in vals), sum(v not in (None, 0) for v in vals), round(float(s), 6)) == (269, 86, -0.065066))
        check("panel(4): sum far from a 6-place boundary", abs(float(s) * 1e6 - round(float(s) * 1e6) ) < 0.4 and r6_margin([s]) > 0.05)
        check("panel(4): no average gap under 1e-6 (no float tie can flip)", float(min(gaps)) > 1e-6)
    else:
        check("panel(2): 285 rows", len(df) == 285)
print("failures:", bad)
sys.exit(1 if bad else 0)
