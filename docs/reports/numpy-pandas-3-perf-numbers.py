"""numpy-pandas level 3 performance task `h-trend-shares`: recompute every number and grade every route.

Run with the session venv (pandas 2.2.3), from anywhere:
    <venv>/bin/python -I docs/reports/numpy-pandas-3-perf-numbers.py
It mirrors the code widget harness, runs the shipped solution and a plain-list loop route against every test
(each expect computed twice), checks the starter fails every test and each planted slip fails one or more,
and recomputes the toy figures with exact fractions. Exits 0 only if every check passes.
"""
# ---- harness: mirrors app/js/engine/widgets/code.js (__zq_case, __zq_cmp, item 700 NaN and DataFrame rules) ----
import json, math, time, multiprocessing as mp, warnings, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _flat(v):
    if hasattr(v, "to_numpy") and getattr(v, "ndim", 0) == 2:
        return v.to_numpy().tolist()
    return v.tolist() if hasattr(v, "tolist") and not isinstance(v, (int, float, complex, str)) else v


def _nan(v):
    try:
        return bool(v != v)
    except Exception:
        return False


def _same(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    if _nan(x) and _nan(y):
        return True
    return bool(x == y)


def _close(x, y, tol):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_close(x[k], y[k], tol) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    if _nan(x) and _nan(y):
        return True
    try:
        rt, at = tol if tol else (1e-9, 1e-12)
        return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
    except Exception:
        return x == y


def _frame_ok(a, e):
    if hasattr(e, "columns") and hasattr(e, "index"):
        return hasattr(a, "columns") and hasattr(a, "index") and _same(list(a.index), list(e.index)) and _same(list(a.columns), list(e.columns))
    return True


def _run(src, pre, cases, q):
    warnings.simplefilter("ignore")
    g = {"__name__": "__main__", "__learner_source__": src}
    out = []
    try:
        if pre:
            exec(compile(pre, "<prelude>", "exec"), g)
        exec(compile(src, "solution.py", "exec"), g)
    except Exception as e:
        q.put([("load-error", repr(e)[:80], 0.0)] * len(cases))
        return
    for c in cases:
        t0 = time.time()
        try:
            if c.get("setup"):
                exec(c["setup"], g)
            a = eval(c["call"], g)
            e = eval(c["expect"], g)
            cmp = c.get("compare", "equal")
            if not _frame_ok(a, e):
                ok = False
            elif cmp == "isclose":
                t = c.get("tol")
                ok = _close(a, e, [t.get("rel", 0), t.get("abs", 0)] if isinstance(t, dict) else None)
            else:
                try:
                    ok = _same(a, e)
                except Exception:
                    ok = False
            val = repr(a)[:100]
        except Exception as x:
            ok, val = False, "error " + type(x).__name__ + ": " + str(x)[:60]
        out.append(("pass" if ok else "FAIL", val, time.time() - t0))
    q.put(out)


def run(widget, src, which="tests", timeout=120):
    cases = widget["examples"] if which == "examples" else widget["tests"]
    q = mp.Queue()
    p = mp.Process(target=_run, args=(src, widget.get("prelude", ""), cases, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return [("timeout", "", timeout)] * len(cases)
    return q.get()


def fails(widget, src, which="tests"):
    r = run(widget, src, which)
    return [i + 1 for i, x in enumerate(r) if x[0] != "pass"], r


def load_item(course, fname, iid):
    d = json.loads((ROOT / "app" / "content" / "courses" / course / fname).read_text(encoding="utf-8"))
    for it in d["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


FAILS = []


def check(name, cond, detail=""):
    print(("ok    " if cond else "FAIL  ") + name + (("  " + str(detail)) if detail and not cond else ""))
    if not cond:
        FAILS.append(name)
# ---- end harness ----

# ---- the item ----
ITEM = load_item("numpy-pandas", "homework-3.json", "h-trend-shares")
W = ITEM["widget"]
SOL = W["solution"]

# A second route: plain Python lists per share, means by sum over slices; pandas only to read df and wrap the answer.
LOOP = '''
import pandas as pd

def trend_returns(df, fast, slow):
    out = {}
    for t in sorted(set(df["ticker"])):
        rows = sorted(((d, i, c) for d, i, c, k in zip(df["date"], df.index, df["close"], df["ticker"]) if k == t))
        c = [r[2] for r in rows]
        pos = []
        for n in range(len(c)):
            if n + 1 >= slow:
                f = sum(c[n + 1 - fast:n + 1]) / fast
                s = sum(c[n + 1 - slow:n + 1]) / slow
                pos.append(1 if f > s else 0)
            else:
                pos.append(0)
        for n, r in enumerate(rows):
            out[r[1]] = float("nan") if n == 0 else pos[n - 1] * (c[n] / c[n - 1] - 1)
    return pd.Series([out[i] for i in df.index], index=df.index)
'''

def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

NOSORT_NOGROUP = '''
import pandas as pd

def trend_returns(df, fast, slow):
    c = df["close"]
    pos = (c.rolling(fast).mean() > c.rolling(slow).mean()).astype(int)
    return pos.shift(1) * c.pct_change()
'''
DATESORT_NOGROUP = NOSORT_NOGROUP.replace('    c = df["close"]\n', '    s = df.sort_values("date")\n    c = s["close"]\n').replace("return pos.shift(1) * c.pct_change()", "return (pos.shift(1) * c.pct_change()).reindex(df.index)")
TICKERSORT_NOGROUP = DATESORT_NOGROUP.replace('df.sort_values("date")', 'df.sort_values(["ticker", "date"])')
WIDE = '''
import pandas as pd

def trend_returns(df, fast, slow):
    wide = df.pivot(index="date", columns="ticker", values="close").sort_index()
    pos = (wide.rolling(fast).mean() > wide.rolling(slow).mean()).astype(int)
    strat = pos.shift(1) * wide.pct_change(fill_method=None)
    long = strat.stack(future_stack=True).rename("q").reset_index()
    m = df.merge(long, on=["date", "ticker"], how="left")
    return pd.Series(m["q"].to_numpy(), index=df.index)
'''
INPLACE = '''
import pandas as pd

def trend_returns(df, fast, slow):
    df.sort_values("date", inplace=True)
    g = df.groupby("ticker")["close"]
    df["f"] = g.transform(lambda c: c.rolling(fast).mean())
    df["w"] = g.transform(lambda c: c.rolling(slow).mean())
    df["pos"] = (df["f"] > df["w"]).astype(int)
    held = df.groupby("ticker")["pos"].shift(1)
    return held * g.pct_change()
'''
PLANTS = {
    "no lag: position times the same row's return": variant("(held * ret)", "(pos * ret)"),
    "shift(-1): tomorrow's position": variant("pos.groupby(s[\"ticker\"]).shift(1)", "pos.groupby(s[\"ticker\"]).shift(-1)"),
    "forward return on the decision row": variant("(held * ret)", "(pos * ret.groupby(s[\"ticker\"]).shift(-1))"),
    "no sort, no groupby": NOSORT_NOGROUP,
    "sorted by date, no groupby": DATESORT_NOGROUP,
    "sorted by ticker then date, no groupby": TICKERSORT_NOGROUP,
    "position shifted without groupby": variant("pos.groupby(s[\"ticker\"]).shift(1)", "pos.shift(1)"),
    "returns without groupby": variant("ret = g.pct_change()", "ret = s[\"close\"].pct_change()"),
    "no sort by date": variant('s = df.sort_values("date")', "s = df"),
    "min_periods=1: signals before the window is full": variant("c.rolling(slow).mean()", "c.rolling(slow, min_periods=1).mean()"),
    ">= instead of >": variant("(f > w)", "(f >= w)"),
    "fast and slow swapped": variant("(f > w)", "(w > f)"),
    "one average: close above the slow mean": variant("(f > w)", "(s[\"close\"] > w)"),
    "centred windows": variant("c.rolling(fast).mean()", "c.rolling(fast, center=True).mean()").replace("c.rolling(slow).mean()", "c.rolling(slow, center=True).mean()"),
    "first row 0, not NaN": variant("(held * ret).reindex(df.index)", "(held * ret).fillna(0).reindex(df.index)"),
    "wide pivot, table dates not share rows": WIDE,
    "sorts and adds columns to df in place": INPLACE,
    "index lost: result in sorted order": variant("(held * ret).reindex(df.index)", "(held * ret).reset_index(drop=True)"),
}
for k, v in PLANTS.items():
    assert v != SOL, k

if __name__ == "__main__":
    from fractions import Fraction as F
    n_t, n_e = len(W["tests"]), len(W["examples"])
    check("11 tests, 1 example, examples are tests", n_t == 11 and n_e == 1 and all(e in W["tests"] for e in W["examples"]))
    check("how says 11 hidden tests", "11 hidden tests" in W["how"])
    f, r = fails(W, SOL)
    check("shipped solution passes every test", not f, f)
    check("shipped solution passes the example", not fails(W, SOL, "examples")[0])
    print(f"      slowest case {max(x[2] for x in r):.3f} s (CPython)")
    f, _ = fails(W, LOOP)
    check("loop route passes every test (second computation of every expect)", not f, f)
    f, _ = fails(W, W["starter"])
    check("starter fails every test", f == list(range(1, n_t + 1)), f)
    for name, src in PLANTS.items():
        f, _ = fails(W, src)
        check(f"plant '{name}' fails tests {f}", bool(f))
    # hand arithmetic with exact fractions on toy()
    K = [40, 41, 44, 43, 42, 45, 41, 43, 46]
    L = [80, 78, 77, 79, 76, 75, 78, 80, 79]
    def held(c, fa, sl):
        return [int(n + 1 >= sl and F(sum(c[n + 1 - fa:n + 1]), fa) > F(sum(c[n + 1 - sl:n + 1]), sl)) for n in range(len(c))]
    hk = held(K, 2, 4)
    check("KTX held after the 5, 10 and 12 Sep closes (fast 2, slow 4); the last earns nothing", hk == [0, 0, 0, 1, 0, 0, 1, 0, 1], hk)
    check("KTX on 6 Sep and 9 Sep: fast = slow exactly (42.5, 43.5)", F(K[3] + K[4], 2) == F(sum(K[1:5]), 4) == F(85, 2) and F(K[4] + K[5], 2) == F(sum(K[2:6]), 4))
    check("KTX 4 Sep: 42.5 > 41.67 with a partial window (min_periods slip holds)", F(K[1] + K[2], 2) > F(sum(K[:3]), 3))
    check("LMN held after 11 Sep close only", held(L, 2, 4) == [0, 0, 0, 0, 0, 0, 0, 1, 1])
    check("returns: 42/43-1, 43/41-1, 79/80-1", [round(42 / 43 - 1, 6), round(43 / 41 - 1, 6), round(79 / 80 - 1, 6)] == [-0.023256, 0.04878, -0.0125])
    K7 = K[:3] + K[4:]
    check("test 7: KTX without 5 Sep held after the 6, 9 and 12 Sep closes; 45/42-1, 41/45-1", held(K7, 2, 4) == [0, 0, 0, 1, 1, 0, 0, 1]
          and [round(45 / 42 - 1, 6), round(41 / 45 - 1, 6)] == [0.071429, -0.088889])
    check("test 8: fast 3, slow 5 held after 6, 9 and 11 Sep; 46/43-1", held(K, 3, 5) == [0, 0, 0, 0, 1, 1, 0, 1, 0] and round(46 / 43 - 1, 6) == 0.069767,
          held(K, 3, 5))
    check("test 6: flat 30s tie, 33 after", held([30] * 5 + [33], 2, 4) == [0] * 5 + [1])
    check("table canvas matches toy()", [[r[1], r[2]] for r in ITEM["canvas"]["params"]["rows"]] == [[f"{k:.2f}", f"{l:.2f}"] for k, l in zip(K, L)])
    ns = {}
    exec(W["prelude"], ns)
    toy = ns["toy"]()
    check("toy() closes match the hand lists", toy[toy.ticker == "KTX"]["close"].tolist() == K and toy[toy.ticker == "LMN"]["close"].tolist() == L)
    check("toy() dates are 2 to 12 September 2024, business days", [d.strftime("%d %b") for d in sorted(toy["date"].unique())] ==
          ["02 Sep", "03 Sep", "04 Sep", "05 Sep", "06 Sep", "09 Sep", "10 Sep", "11 Sep", "12 Sep"])
    p4 = ns["panel"](4)
    check("panel(4): five shares, 60 days, some days missing", p4["ticker"].nunique() == 5 and p4["date"].nunique() == 60 and len(p4) < 300, len(p4))
    check("test 11: 16 returns in toy() (8 a share)", 2 * (9 - 1) == 16)
    print(f"\nfailures: {len(FAILS)}")
    raise SystemExit(1 if FAILS else 0)
