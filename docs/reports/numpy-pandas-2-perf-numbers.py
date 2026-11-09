"""numpy-pandas level 2 performance task `h-fills-report`: recompute every number and grade every route.

Run with the session venv (pandas 2.2.3), from anywhere:
    <venv>/bin/python -I docs/reports/numpy-pandas-2-perf-numbers.py
It mirrors the code widget harness, runs the shipped solution and a plain-loop route against every test
(each expect computed twice), checks the starter fails every test and each planted slip fails one or more,
and recomputes the numbers in the prose and feedback by hand. Exits 0 only if every check passes.
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
ITEM = load_item("numpy-pandas", "homework-2.json", "h-fills-report")
W = ITEM["widget"]
SOL = W["solution"]

# A second route: plain Python loops for every number; pandas only wraps the finished lists.
LOOP = '''
import pandas as pd

def fills_report(ids, ticker, side, qty, price, a, b):
    signed = [(-q if s == "sell" else q) for s, q in zip(side, qty)]
    value = [float("nan") if p is None else q * p for q, p in zip(signed, price)]
    i, j = ids.index(a), ids.index(b)
    span_ids = ids[i:j + 1]
    span = pd.Series(value[i:j + 1], index=span_ids)
    conf = [k for k in range(len(ids)) if price[k] is not None]
    net = 0.0
    for k in conf:
        net += value[k]
    fills = pd.DataFrame({"ticker": list(ticker), "qty": signed, "value": value}, index=list(ids))
    return {"fills": fills, "span": span, "last": ids[conf[-1]], "net": net}
'''

# Planted slips: each must fail at least one hidden test.
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

PLANTS = {
    "chained assignment fills[mask]['qty'] *= -1": variant('fills.loc[fills["side"] == "sell", "qty"] *= -1', 'fills[fills["side"] == "sell"]["qty"] *= -1'),
    "index sorted by trade id": variant('}, index=ids)', '}, index=ids).sort_index()'),
    "span by position, iloc[a:b]": variant('fills.loc[a:b, "value"]', 'fills["value"].iloc[a:b]'),
    "span by position, iloc[a:b + 1]": variant('fills.loc[a:b, "value"]', 'fills["value"].iloc[a:b + 1]'),
    "span by plain brackets fills[a:b]": variant('fills.loc[a:b, "value"]', 'fills[a:b]["value"]'),
    "span drops unconfirmed fills": variant('fills.loc[a:b, "value"]', 'fills["value"].dropna().loc[a:b]'),
    "last = last fill, confirmed or not": variant('confirmed.index[-1]', 'fills.index[-1]'),
    "last = largest confirmed id": variant('confirmed.index[-1]', 'confirmed.index.max()'),
    "price gaps filled with 0": variant('fills["qty"] * fills["price"]', 'fills["qty"] * fills["price"].fillna(0)'),
    "value from unsigned qty": SOL.replace('    fills.loc[fills["side"] == "sell", "qty"] *= -1          # one .loc call writes into fills itself\n    fills["value"] = fills["qty"] * fills["price"]          # NaN where the price is missing\n',
                                           '    fills["value"] = fills["qty"] * fills["price"]\n    fills.loc[fills["side"] == "sell", "qty"] *= -1\n'),
    "net by Python sum over all values (NaN)": variant('float(confirmed.sum())', 'float(sum(fills["value"]))'),
    "signs the caller's qty list in place": SOL.replace('    fills = pd.DataFrame(', '    for k in range(len(qty)):\n        if side[k] == "sell":\n            qty[k] = -qty[k]\n    fills = pd.DataFrame(').replace('    fills.loc[fills["side"] == "sell", "qty"] *= -1          # one .loc call writes into fills itself\n', ''),
    "span as a list, not a Series": variant('"span": span,', '"span": span.tolist(),'),
}
for k, v in PLANTS.items():
    assert v != SOL, k

if __name__ == "__main__":
    n_t, n_e = len(W["tests"]), len(W["examples"])
    check("13 tests, 1 example, examples are tests", n_t == 13 and n_e == 1 and all(e in W["tests"] for e in W["examples"]))
    check("how says 13 hidden tests", "13 hidden tests" in W["how"])
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
    # hand arithmetic for day(), the numbers in the prose and feedback
    q = [1000, 2500, -400, 60, -1500, 300, -60]
    p = [2.10, 0.70, 2.15, 27.50, None, 2.05, None]
    v = [None if b is None else round(a * b, 9) for a, b in zip(q, p)]
    check("values by hand: 2100, 1750, -860, 1650, -, 615, -", v == [2100.0, 1750.0, -860.0, 1650.0, None, 615.0, None], v)
    check("net by hand 2100 + 1750 - 860 + 1650 + 615 = 5255", 2100 + 1750 - 860 + 1650 + 615 == 5255)
    check("byKey test-7 says £5,255", "£5,255" in ITEM["feedback"]["byKey"]["test-7"])
    check("day() has seven fills (prose 'seven fills')", "seven fills" in ITEM["prose"])
    ns = {}
    exec(W["prelude"], ns)
    ids, tk, sd, qt, pr = ns["book"](5, 40)
    a, b = ids[6], ids[29]
    inside = pr[6:30]
    check("book(5, 40): 12 unconfirmed, 6 inside positions 6 to 29", sum(x is None for x in pr) == 12 and sum(x is None for x in inside) == 6,
          (sum(x is None for x in pr), sum(x is None for x in inside)))
    check("byKey test-12 says 12 and 7", "12 fills are unconfirmed and 6 of them" in ITEM["feedback"]["byKey"]["test-12"])
    ids7 = ns["book"](7, 40)[0]
    check("book ids are 1 to 40 shuffled", sorted(ids7) == list(range(1, 41)) and ids7 != sorted(ids7))
    check("table canvas rows match day()", [[r[0], r[1], r[2], r[3], r[4]] for r in ITEM["canvas"]["params"]["rows"]] ==
          [[str(i), t, s, str(qq), "None" if pp is None else f"{pp:.2f}"] for i, t, s, qq, pp in zip(*ns["day"]())])
    print(f"\nfailures: {len(FAILS)}")
    raise SystemExit(1 if FAILS else 0)
