"""plotting level 3 performance task `h-price-file-report`: recompute every number and grade every route.

Run with the session venv (matplotlib 3.8.4, pandas 2.2.3, the Pyodide versions), from anywhere:
    <venv>/bin/python -I docs/reports/plotting-3-perf-numbers.py
It mirrors the code widget harness (prelude, learner code, each case's setup, call and __zq_cmp with tol),
runs the shipped solution and a csv-and-loops route against every test, checks the starter fails every test
and each planted slip fails at least one, recomputes every expect by a third route (exact fractions), and
checks the numbers in the prose, feedback and explanation. Saved PNGs go to a temporary folder.
Exits 0 only if every check passes.
"""
import json, math, time, pathlib, warnings, os, tempfile, statistics, multiprocessing as mp
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[2]


# ---- harness: mirrors app/js/engine/widgets/code.js (__zq_case, __zq_cmp) ----
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
            if c.get("compare", "equal") == "isclose":
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


FAILS = []


def check(name, cond, detail=""):
    print(("ok    " if cond else "FAIL  ") + name + (("  " + str(detail)) if detail and not cond else ""))
    if not cond:
        FAILS.append(name)
# ---- end harness ----


d = json.loads((ROOT / "app/content/courses/plotting/homework-3.json").read_text(encoding="utf-8"))
ITEM = [it for it in d["items"] if it["id"] == "h-price-file-report"][0]
W = ITEM["widget"]
SOL = W["solution"]

# Second route: csv module, sorted dict, statistics.stdev and a running-peak loop; no pandas maths.
LOOP = '''import csv, io, math, statistics
import matplotlib.pyplot as plt
from datetime import date


def report_figure(text, path):
    byday = {}
    for row in csv.DictReader(io.StringIO(text)):
        byday[date.fromisoformat(row["date"])] = float(row["close"])
    days = sorted(byday)
    c = [byday[x] for x in days]
    rets = [c[i] / c[i - 1] - 1 for i in range(1, len(c))]
    vol = [statistics.stdev(rets[i - 4:i + 1]) * math.sqrt(252) for i in range(4, len(rets))]
    peak, dd = c[0], []
    for p in c:
        peak = max(peak, p)
        dd.append(p / peak - 1)
    k = dd.index(min(dd))
    fig, axes = plt.subplots(3, 1, sharex=True)
    axes[0].plot(days[1:], rets)
    axes[1].plot(days[5:], vol)
    axes[2].plot(days, dd)
    axes[2].annotate(f"Max drawdown {dd[k]:.1%}", xy=(days[k], dd[k]), xytext=(days[0], dd[k]), arrowprops={"arrowstyle": "->"})
    v = statistics.stdev(rets) * math.sqrt(252)
    fig.suptitle(f"Volatility {v:.1%}, max drawdown {dd[k]:.1%}")
    fig.savefig(path, dpi=150)
    return fig, axes
'''


def swap(src, old, new):
    assert old in src, old
    return src.replace(old, new)


PLANTS = {
    "rows left in file order": swap(SOL, '["close"].sort_index()', '["close"]'),
    "repeated day kept": swap(SOL, 'df.drop_duplicates("date")', "df"),
    "both copies of the repeated day dropped": swap(SOL, 'df.drop_duplicates("date")', 'df.drop_duplicates("date", keep=False)'),
    "duplicates judged by close alone": swap(SOL, 'df.drop_duplicates("date")', 'df.drop_duplicates("close")'),
    "returns on the earlier date": swap(SOL, "axes[0].plot(rets.index, rets.values)", "axes[0].plot(closes.index[:-1], rets.values)"),
    "population sd in the rolling window": swap(SOL, "rets.rolling(5).std()", "rets.rolling(5).std(ddof=0)"),
    "rolling volatility times 252": swap(SOL, "rets.rolling(5).std() * np.sqrt(252)", "rets.rolling(5).std() * 252"),
    "drawdown from the overall top": swap(SOL, "closes.cummax()", "closes.max()"),
    "arrow at the lowest close": swap(SOL, "t, mdd = dd.idxmin(), dd.min()", "t, mdd = closes.idxmin(), dd.min()"),
    "panels not sharing x": swap(SOL, "sharex=True, ", ""),
    "dates left as text": swap(SOL, ', parse_dates=["date"]', ""),
    "saved at the default dpi": swap(SOL, "dpi=150, ", ""),
    "not saved": swap(SOL, '    fig.savefig(path, dpi=150, bbox_inches="tight")\n', ""),
    "title volatility from the population sd": swap(SOL, "{rets.std() * np.sqrt(252):.1%}", "{rets.std(ddof=0) * np.sqrt(252):.1%}"),
    "title volatility from the last rolling value": swap(SOL, "{rets.std() * np.sqrt(252):.1%}", "{vol.iloc[-1]:.1%}"),
    "arrow label without its sign": swap(SOL, 'axes[2].annotate(f"Max drawdown {mdd:.1%}"', 'axes[2].annotate(f"Max drawdown {-mdd:.1%}"'),
}
# correct variants that must pass: the first return left as NaN, and a fixed file name ignored by no test
VARIANTS = {
    "first return kept as NaN": swap(SOL, "closes.pct_change().dropna()", "closes.pct_change()"),
    "whole-row drop_duplicates": swap(SOL, 'df.drop_duplicates("date")', "df.drop_duplicates()"),
}


def exact(text):
    """Third route: exact fractions from the printed closes."""
    seen = {}
    for line in text.strip().split("\n")[1:]:
        k, v = line.split(",")
        seen[k] = Fraction(v)
    days = sorted(seen)
    c = [seen[k] for k in days]
    r = [c[i] / c[i - 1] - 1 for i in range(1, len(c))]

    def sd(xs):
        m = sum(xs) / len(xs)
        return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    vol = [[days[i + 1], sd(r[i - 4:i + 1]) * math.sqrt(252)] for i in range(4, len(r))]
    peak, dd = c[0], []
    for k, p in zip(days, c):
        peak = max(peak, p)
        dd.append([k, p / peak - 1])
    j = min(range(len(dd)), key=lambda i: dd[i][1])
    return {"days": days, "c": c, "rets": [[k, x] for k, x in zip(days[1:], r)], "vol": vol, "dd": dd, "trough": dd[j],
            "v": sd(r) * math.sqrt(252)}


def near(pts, exp, tol=2e-6):
    return len(pts) == len(exp) and all(a[0] == b[0] and abs(float(a[1]) - float(b[1])) <= tol for a, b in zip(pts, exp))


if __name__ == "__main__":
    os.chdir(tempfile.mkdtemp(prefix="plotting-3-perf-"))
    n_t, n_e = len(W["tests"]), len(W["examples"])
    check("10 tests, 1 example, strictly more tests than examples", (n_t, n_e) == (10, 1))
    check("performance kind is code", ITEM.get("performance") == "code")
    check("every example is one of the tests", all(e in W["tests"] for e in W["examples"]))
    check("how says 10 hidden tests", "10 hidden tests" in W["how"])
    check("byKey covers test-1 to test-10 exactly", sorted(ITEM["feedback"]["byKey"]) == sorted(f"test-{i}" for i in range(1, 11)))

    f, r = fails(W, SOL)
    check("solution passes every test", not f, [x for x in r if x[0] != "pass"])
    print(f"      slowest case {max(x[2] for x in r):.3f} s (CPython)")
    f, _ = fails(W, SOL, "examples")
    check("solution passes the example", not f, f)
    f, r = fails(W, LOOP)
    check("csv-and-loops route passes every test", not f, [x for x in r if x[0] != "pass"])
    for name, src in VARIANTS.items():
        f, _ = fails(W, src)
        check(f"correct variant '{name}' passes", not f, f)
    f, _ = fails(W, W["starter"])
    check("starter fails every test", f == list(range(1, n_t + 1)), f)
    caught = 0
    for name, src in PLANTS.items():
        f, _ = fails(W, src)
        check(f"plant '{name}' fails tests {f}", bool(f))
        caught += bool(f)
    check("at least three planted slips caught", caught >= 3)

    # third route for every expect
    ns = {}
    exec(W["prelude"], ns)
    A, B = exact(ns["vendor_file"]()), exact(ns["price_file"](7, 40))
    T = W["tests"]
    check("test 2 expect: vendor returns by exact fractions", near(eval(T[1]["expect"]), A["rets"]))
    check("test 3 expect: vendor rolling volatility by exact variance", near(eval(T[2]["expect"]), A["vol"]))
    check("test 4 expect: vendor drawdown by exact fractions", near(eval(T[3]["expect"]), A["dd"]))
    e5 = eval(T[4]["expect"])
    check("test 5 expect: arrow text, date and depth", e5[0] == f"Max drawdown {float(A['trough'][1]):.1%}" and e5[1] == A["trough"][0]
          and abs(e5[2] - float(A["trough"][1])) <= 1e-6, e5)
    check("test 6 expect: vendor title", eval(T[5]["expect"]) == f"Volatility {A['v']:.1%}, max drawdown {float(A['trough'][1]):.1%}")
    check("test 8 expect: price_file(7, 40) has 39 returns, 2 September to its last day",
          eval(T[7]["expect"]) == [39, "2025-09-02", B["days"][-1]] and len(B["rets"]) == 39)
    check("test 9 expect: price_file(7, 40) arrow", eval(T[8]["expect"]) == [f"Max drawdown {float(B['trough'][1]):.1%}", B["trough"][0]])
    check("test 10 expect: price_file(7, 40) title", eval(T[9]["expect"]) == f"Volatility {B['v']:.1%}, max drawdown {float(B['trough'][1]):.1%}")
    txt = ns["price_file"](7, 40).strip().split("\n")[1:]
    check("price_file(7, 40): 41 rows, newest first, one day twice", len(txt) == 41 and len(set(txt)) == 40
          and [x.split(",")[0] for x in txt[:40]] == sorted([x.split(",")[0] for x in txt[:40]], reverse=True))

    # the vendor file and the table canvas
    vt = ns["vendor_file"]().strip().split("\n")
    rows = [x.split(",") for x in vt[1:]]
    check("table canvas rows are the vendor file's rows, in order", ITEM["canvas"]["params"]["rows"] == rows and vt[0] == "date,close")
    check("vendor file: 19 rows, 18 days, only 16 March repeated", len(rows) == 19 and len({r[0] for r in rows}) == 18
          and [k for k in {r[0] for r in rows} if sum(r[0] == k for r in rows) > 1] == ["2026-03-16"])
    check("vendor file: two different days share the close 42.50", sorted(r[0] for r in rows if r[1] == "42.50") == ["2026-03-09", "2026-03-13"])
    check("vendor file is not in date order", [r[0] for r in rows] != sorted(r[0] for r in rows))

    # numbers in the prose, feedback and explanation
    peak_i = A["c"].index(max(A["c"]))
    check("running peak £44.80 on 11 March", A["c"][peak_i] == Fraction("44.80") and A["days"][peak_i] == "2026-03-11")
    check("trough 17 March, £40.10, -10.5% (40.10 / 44.80 - 1)", A["trough"][0] == "2026-03-17" and A["trough"][1] == Fraction("40.10") / Fraction("44.80") - 1
          and f"{float(A['trough'][1]):.1%}" == "-10.5%")
    low_i = A["c"].index(min(A["c"]))
    low_dd = A["c"][low_i] / max(A["c"][:low_i + 1]) - 1
    check("lowest close £38.90 on 4 March, 5.6% below its peak £41.20", A["c"][low_i] == Fraction("38.90") and A["days"][low_i] == "2026-03-04"
          and max(A["c"][:low_i + 1]) == Fraction("41.20") and round(float(-low_dd) * 100, 1) == 5.6)
    check("17 returns, the first on 3 March; volatility starts 9 March", len(A["rets"]) == 17 and A["rets"][0][0] == "2026-03-03" and A["vol"][0][0] == "2026-03-09")
    check("the fifth return is on 9 March (prose 'starts on the fifth return')", A["rets"][4][0] == "2026-03-09")
    v2 = statistics.stdev([float(x) for _, x in A["rets"]]) * math.sqrt(252)
    check("vendor volatility 45.2% by exact variance and by statistics.stdev", f"{A['v']:.1%}" == f"{v2:.1%}" == "45.2%")
    v3 = statistics.stdev([float(x) for _, x in B["rets"]]) * math.sqrt(252)
    check("price_file(7, 40) volatility by both routes", f"{B['v']:.1%}" == f"{v3:.1%}")
    ex = ITEM["explain"]["text"]
    check("explain names 18 days, 17 returns, £44.80, £40.10, 10.5% below, £38.90, 5.6%, 45.2%",
          all(s in ex for s in ("18 days", "17 returns", "£44.80", "£40.10", "10.5% below it", "£38.90", "5.6%", "45.2%")))
    bk = ITEM["feedback"]["byKey"]
    check("byKey numbers: 17 and 3 March, 9 March, 10.5% 17 March 4 March, title, 39 and 2 September",
          "17 returns, the first on 3 March" in bk["test-2"] and "9 March" in bk["test-3"]
          and all(s in bk["test-5"] for s in ("10.5%", "17 March", "4 March")) and "Volatility 45.2%, max drawdown -10.5%" in bk["test-6"]
          and "39 returns run from 2 September" in bk["test-8"])
    check("150 dpi is 5906 pixels a metre, read back as 150", round(round(150 / 0.0254) * 0.0254) == 150 and round(150 / 0.0254) == 5906)
    print(f"\nfailures: {len(FAILS)}")
    raise SystemExit(1 if FAILS else 0)
