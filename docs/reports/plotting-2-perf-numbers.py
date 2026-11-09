"""plotting level 2 performance task `h-wealth-peak`: recompute every number and grade every route.

Run with the session venv (matplotlib 3.8.4, pandas 2.2.3, the Pyodide versions), from anywhere:
    <venv>/bin/python -I docs/reports/plotting-2-perf-numbers.py
It mirrors the code widget harness (prelude, learner code, each case's setup, call and __zq_cmp with tol),
runs the shipped solution and a plain-loop route against every test, checks the starter fails every test and
each planted slip fails at least one, recomputes every expect by a third route (exact fractions), and checks
the numbers in the prose, feedback and explanation. Exits 0 only if every check passes.
"""
import json, math, time, pathlib, warnings, multiprocessing as mp
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


d = json.loads((ROOT / "app/content/courses/plotting/homework-2.json").read_text(encoding="utf-8"))
ITEM = [it for it in d["items"] if it["id"] == "h-wealth-peak"][0]
W = ITEM["widget"]
SOL = W["solution"]

HEAD = "import matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\n"

# Second route: a plain loop over the sorted years, no cumprod and no accumulate.
LOOP = HEAD + '''
def wealth_chart(rets, capital):
    pairs = sorted(zip(rets.index.tolist(), rets.tolist()))
    years, wealth, peak = [pairs[0][0] - 1], [float(capital)], [float(capital)]
    for y, r in pairs:
        years.append(y)
        wealth.append(wealth[-1] * (1 + r))
        peak.append(max(peak[-1], wealth[-1]))
    fig, ax = plt.subplots()
    ax.plot(years, wealth, label="Wealth")
    ax.plot(years, peak, "--", label="Running peak")
    ax.set_yscale("log")
    ax.set_ylabel("£")
    ax.legend()
    return ax
'''


def plant(body):
    return HEAD + "\ndef wealth_chart(rets, capital):\n" + body


GOOD_TAIL = '''    fig, ax = plt.subplots()
    ax.plot(years, wealth, label="Wealth")
    ax.plot(years, peak, linestyle="--", label="Running peak")
    ax.set_yscale("log")
    ax.set_ylabel("Wealth (£)")
    ax.legend()
    return ax
'''
SORTED = '''    r = rets.sort_index()
    years = [r.index[0] - 1] + list(r.index)
    wealth = capital * np.cumprod(np.r_[1.0, 1 + r.to_numpy()])
    peak = np.maximum.accumulate(wealth)
'''
PLANTS = {
    "years left unsorted": plant('''    r = rets
    years = [r.index.min() - 1] + list(r.index)
    wealth = capital * np.cumprod(np.r_[1.0, 1 + r.to_numpy()])
    peak = np.maximum.accumulate(wealth)
''' + GOOD_TAIL),
    "no opening point": plant('''    r = rets.sort_index()
    years = list(r.index)
    wealth = capital * np.cumprod(1 + r.to_numpy())
    peak = np.maximum.accumulate(wealth)
''' + GOOD_TAIL),
    "wealth of £1, capital ignored": plant('''    r = rets.sort_index()
    years = [r.index[0] - 1] + list(r.index)
    wealth = np.cumprod(np.r_[1.0, 1 + r.to_numpy()])
    peak = np.maximum.accumulate(wealth)
''' + GOOD_TAIL),
    "peak taken before the opening point is added": plant('''    r = rets.sort_index()
    years = [r.index[0] - 1] + list(r.index)
    w = capital * np.cumprod(1 + r.to_numpy())
    wealth = np.r_[capital, w]
    peak = np.r_[capital, np.maximum.accumulate(w)]
''' + GOOD_TAIL),
    "linear y axis": plant(SORTED + GOOD_TAIL.replace('    ax.set_yscale("log")\n', "")),
    "legend called before the peak is drawn": plant(SORTED + '''    fig, ax = plt.subplots()
    ax.plot(years, wealth, label="Wealth")
    ax.legend()
    ax.plot(years, peak, linestyle="--", label="Running peak")
    ax.set_yscale("log")
    ax.set_ylabel("Wealth (£)")
    return ax
'''),
    "lines labelled, no legend": plant(SORTED + GOOD_TAIL.replace("    ax.legend()\n", "")),
    "peak as one flat line at the top": plant(SORTED + '''    fig, ax = plt.subplots()
    ax.plot(years, wealth, label="Wealth")
    ax.axhline(wealth.max(), linestyle="--", label="Running peak")
    ax.set_yscale("log")
    ax.set_ylabel("Wealth (£)")
    ax.legend()
    return ax
'''),
    "sorts the caller's Series in place": plant('''    rets.sort_index(inplace=True)
    r = rets
    years = [r.index[0] - 1] + list(r.index)
    wealth = capital * np.cumprod(np.r_[1.0, 1 + r.to_numpy()])
    peak = np.maximum.accumulate(wealth)
''' + GOOD_TAIL),
    "adds returns instead of compounding": plant('''    r = rets.sort_index()
    years = [r.index[0] - 1] + list(r.index)
    wealth = capital * (1 + np.cumsum(np.r_[0.0, r.to_numpy()]))
    peak = np.maximum.accumulate(wealth)
''' + GOOD_TAIL),
    "axes swapped": plant(SORTED + GOOD_TAIL.replace("ax.plot(years, wealth,", "ax.plot(wealth, years,").replace("ax.plot(years, peak,", "ax.plot(peak, years,")),
    "peak drawn solid": plant(SORTED + GOOD_TAIL.replace('linestyle="--", ', "")),
    "y label without the unit": plant(SORTED + GOOD_TAIL.replace('"Wealth (£)"', '"Wealth"')),
    "logs plotted on a linear axis": plant(SORTED + GOOD_TAIL.replace("ax.plot(years, wealth,", "ax.plot(years, np.log(wealth),")
                                           .replace("ax.plot(years, peak,", "ax.plot(years, np.log(peak),").replace('    ax.set_yscale("log")\n', "")),
    "capital fixed at £10,000": plant(SORTED.replace("capital *", "10000 *") + GOOD_TAIL),
}


def exact_path(rets, capital):
    """Third route for the expects: exact fractions from the decimal returns, rounded to pence at the end."""
    ys = sorted(rets)
    years, w, pk = [ys[0] - 1], [Fraction(capital)], [Fraction(capital)]
    for y in ys:
        years.append(y)
        w.append(w[-1] * (1 + Fraction(str(rets[y]))))
        pk.append(max(pk[-1], w[-1]))
    return years, w, pk


if __name__ == "__main__":
    n_t, n_e = len(W["tests"]), len(W["examples"])
    check("10 tests, 1 example, strictly more tests than examples", (n_t, n_e) == (10, 1))
    check("performance kind is code", ITEM.get("performance") == "code")
    check("every example is one of the tests", all(e in W["tests"] for e in W["examples"]))
    check("how says 10 hidden tests", "10 hidden tests" in W["how"])
    check("byKey covers test-1 to test-10 exactly", sorted(ITEM["feedback"]["byKey"]) == sorted(f"test-{i}" for i in range(1, 11)))

    f, r = fails(W, SOL)
    check("solution passes every test", not f, f)
    print(f"      slowest case {max(x[2] for x in r):.3f} s (CPython)")
    f, _ = fails(W, SOL, "examples")
    check("solution passes the example", not f, f)
    f, _ = fails(W, LOOP)
    check("loop route passes every test", not f, f)
    f, _ = fails(W, W["starter"])
    check("starter fails every test", f == list(range(1, n_t + 1)), f)
    caught = 0
    for name, src in PLANTS.items():
        f, _ = fails(W, src)
        check(f"plant '{name}' fails tests {f}", bool(f))
        caught += bool(f)
    check("at least three planted slips caught", caught >= 3)

    # third route: the expects themselves, from exact fractions
    ns = {}
    exec(W["prelude"], ns)
    F = ns["fund"]().to_dict()
    S = ns["short"]().to_dict()
    fy, fw, fp = exact_path(F, 10000)
    sy, sw, sp = exact_path(S, 20000)
    pence = lambda xs: [round(float(x), 2) for x in xs]
    T = W["tests"]
    check("test 1 expect is the years 1992 to 2024", eval(T[0]["expect"]) == fy == list(range(1992, 2025)))
    check("test 2 expect is the exact wealth to the penny", _close(eval(T[1]["expect"]), pence(fw), (0, 0.006)))
    check("test 3 expect is the exact running peak to the penny", _close(eval(T[2]["expect"]), pence(fp), (0, 0.006)))
    ex9 = eval(T[8]["expect"])
    check("test 9 expect is short()'s years and wealth", ex9[0] == sy == list(range(2015, 2022)) and _close(ex9[1], pence(sw), (0, 0.006)))
    check("test 10 expect is short()'s running peak", _close(eval(T[9]["expect"]), pence(sp), (0, 0.006)))
    check("fund() is 32 years, 1993 to 2024, not in order", sorted(F) == list(range(1993, 2025)) and list(F) != sorted(F))
    check("short() is 2016 to 2021, not in order", sorted(S) == list(range(2016, 2022)) and list(S) != sorted(S))

    # numbers in the prose, feedback and explanation
    peak99 = fw[fy.index(1999)]
    low02 = fw[fy.index(2002)]
    fall = 1 - low02 / peak99
    dd = [w / p - 1 for w, p in zip(fw, fp)]
    check("max drawdown of fund() is 41.0%, at 2002, from the 1999 peak", round(float(-min(dd)), 3) == 0.410 and fy[dd.index(min(dd))] == 2002
          and fp[fy.index(2002)] == peak99, float(-min(dd)))
    # the same fall by the three yearly returns 2000 to 2002
    fall2 = 1 - (1 + Fraction("-0.081")) * (1 + Fraction("-0.152")) * (1 + Fraction("-0.243"))
    check("41% fall by the returns 2000 to 2002 equals the wealth route", fall == fall2 and round(float(fall2) * 100) == 41)
    check("2024 wealth is £50,792 to the pound", round(float(fw[-1])) == 50792 and fy[-1] == 2024, float(fw[-1]))
    check("2024 wealth by the product of all 32 returns", round(10000 * math.prod(1 + F[y] for y in F)) == 50792)
    check("explain says 41%, 2000 to 2002 and £50,792", all(t in ITEM["explain"]["text"] for t in ("41%", "2000 to 2002", "£50,792")))
    check("short() falls 5% in its first year, 2016", S[2016] == -0.05 and min(S) == 2016)
    check("short() peak stays at £20,000 until 2021", all(p == 20000 for p in sp[:-1]) and sp[-1] > 20000 and sy[-1] == 2021)
    check("short() wealth by hand: 20000 x 0.95 x 0.88 x 1.05 x 1.08 x 0.7 x 1.6 = 21235.7376",
          Fraction(20000) * Fraction("0.95") * Fraction("0.88") * Fraction("1.05") * Fraction("1.08") * Fraction("0.7") * Fraction("1.6") == sw[-1]
          and float(sw[-1]) == 21235.7376)
    check("byKey test-10 says 5% and £20,000 until 2021", all(s in ITEM["feedback"]["byKey"]["test-10"] for s in ("5%", "£20,000", "2021")))
    check("byKey test-6 says 32 years", "32 years" in ITEM["feedback"]["byKey"]["test-6"])
    check("prose names 1992, 1993 to 2024 and 2016 to 2021", all(s in ITEM["prose"] for s in ("1992", "1993 to 2024", "2016 to 2021")))
    # the 30% example in the prose: on a log axis, a 30% fall is the same height wherever it starts
    h = lambda a: math.log10(a) - math.log10(a * 0.7)
    check("a 30% fall has the same log height at £11,342 (1994) and £50,000", math.isclose(h(11341.68), h(50000)) and math.isclose(h(1), -math.log10(0.7)))
    check("the same fall differs on a linear axis", not math.isclose(11341.68 * 0.3, 50000 * 0.3))
    check("1994 wealth is £11,341.68 by hand (10000 x 1.204 x 0.942)", round(10000 * 1.204 * 0.942, 2) == 11341.68 == round(float(fw[2]), 2))

    print(f"\nfailures: {len(FAILS)}")
    raise SystemExit(1 if FAILS else 0)
