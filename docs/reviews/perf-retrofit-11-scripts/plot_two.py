"""plotting L2 h-wealth-peak and L3 h-price-file-report (code: shipped, starter, reader solutions, planted slips,
format margins). Run with the venv Python (NumPy 2.5.4), a NumPy 2.0.2 venv, and Pyodide via pyo11.mjs."""
import sys, pathlib, math, statistics, csv, io
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fractions import Fraction as F
import numpy as np
from harness11 import item, summary, patched

bad = 0
def check(name, ok):
    global bad
    print(("ok   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1
print("numpy", np.__version__, sys.platform)

# ---------- L2
it = item("plotting", "homework-2.json", "h-wealth-peak")
w = it["widget"]; sol = w["solution"]
print("L2 h-wealth-peak")
f, _ = summary(w, sol, "shipped solution", "all"); check("L2 shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("L2 starter fails", len(f) > 0)
mine = r'''
import matplotlib.pyplot as plt
import pandas as pd
def wealth_chart(rets, capital):
    r = rets.sort_index()
    wealth = pd.concat([pd.Series([float(capital)], index=[r.index[0] - 1]), capital * (1 + r).cumprod()])
    peak = wealth.cummax()
    fig, ax = plt.subplots()
    wealth.plot(ax=ax, label="Wealth")
    peak.plot(ax=ax, style="--", label="Running peak")
    ax.semilogy()
    ax.set_ylabel("£ (log scale)")
    ax.legend()
    return ax
'''
f, _ = summary(w, mine, "reader solution (pandas .plot, cummax, semilogy)", "all"); check("L2 reader solution passes", f == [])
loops = r'''
import matplotlib.pyplot as plt
def wealth_chart(rets, capital):
    years = sorted(rets.index)
    xs, ws, ps = [years[0] - 1], [capital], [capital]
    for y in years:
        xs.append(y); ws.append(ws[-1] * (1 + rets[y])); ps.append(max(ps[-1], ws[-1]))
    fig = plt.figure(); ax = fig.add_subplot()
    ax.plot(xs, ws, "-", label="Wealth"); ax.plot(xs, ps, ls="dashed", label="Running peak")
    ax.set_yscale("log"); ax.set_ylabel("Wealth, £"); ax.legend(loc="upper left")
    return ax
'''
f, _ = summary(w, loops, "loop route (sorted years, running max)", "all"); check("L2 loop route passes", f == [])
L2plants = [
    ("years left unsorted", [("r = rets.sort_index()", "r = rets")]),
    ("no opening point", [("years = [r.index[0] - 1] + list(r.index)", "years = list(r.index)"), ("np.r_[1.0, 1 + r.to_numpy()]", "1 + r.to_numpy()")]),
    ("returns added, not compounded", [("capital * np.cumprod(np.r_[1.0, 1 + r.to_numpy()])", "capital * (1 + np.cumsum(np.r_[0.0, r.to_numpy()]))")]),
    ("peak is the overall top", [("peak = np.maximum.accumulate(wealth)", "peak = np.full(len(wealth), wealth.max())")]),
    ("peak starts after the opening year", [("peak = np.maximum.accumulate(wealth)", "peak = np.r_[wealth[1], np.maximum.accumulate(wealth[1:])]")]),
    ("linear axis", [('ax.set_yscale("log")', 'pass')]),
    ("solid peak", [('linestyle="--", ', '')]),
    ("no £ in the label", [('ax.set_ylabel("Wealth (£, log scale)")', 'ax.set_ylabel("Wealth (log scale)")')]),
    ("legend before the peak is drawn", [('    ax.plot(years, peak, linestyle="--", label="Running peak")\n', ''), ('    ax.legend()\n', '    ax.legend()\n    ax.plot(years, peak, linestyle="--", label="Running peak")\n')]),
    ("caller's Series sorted in place", [("r = rets.sort_index()", "rets.sort_index(inplace=True); r = rets")]),
    ("capital fixed at 10,000", [("wealth = capital *", "wealth = 10000 *")]),
    ("logs of wealth on a linear axis", [("ax.plot(years, wealth,", "ax.plot(years, np.log(wealth),"), ("ax.plot(years, peak,", "ax.plot(years, np.log(peak),"), ('ax.set_yscale("log")', 'pass')]),
]
for name, pairs in L2plants:
    f, _ = summary(w, patched(sol, *pairs), "plant: " + name)
    check("L2 plant caught: " + name, len(f) > 0)
# second route for the expects: exact Fractions of the returns
ns = {}; exec(w["prelude"], ns)
for fn, cap, n_ in (("fund", 10000, 33), ("short", 20000, 7)):
    r = ns[fn]().sort_index()
    wv = [F(cap)]
    for v in r:
        wv.append(wv[-1] * (1 + F(str(v))))
    pk = [max(wv[:k + 1]) for k in range(len(wv))]
    ex = [c for c in w["tests"] if fn + "()" in c["setup"]]
    print(f"  {fn}: {len(wv)} points, end £{float(wv[-1]):.2f}, peak end £{float(pk[-1]):.2f}")
    worst = max(abs(float(x * 100) - round(float(x * 100))) for x in wv)
    check(f"{fn}: {n_} points", len(wv) == n_)
    check(f"{fn}: no wealth within 0.1p of a half-penny (so rounding to pence is stable)", all(abs(float((x * 100) % 1) - 0.5) > 0.001 for x in wv))
    if fn == "fund":
        want = eval(w["tests"][1]["expect"]); wantp = eval(w["tests"][2]["expect"])
        check("fund wealth expect equals the exact route", [round(float(x), 2) for x in wv] == want)
        check("fund peak expect equals the exact route", [round(float(x), 2) for x in pk] == wantp)
        dd = wv[10] / max(wv[:11]) - 1
        check("explain: 2000 to 2002 fall of 41% from 24,156.10", abs(float(dd) + 0.41) < 0.005 and round(float(wv[7]), 2) == 24156.10 and round(float(wv[-1])) == 50792)
    else:
        want = eval(w["tests"][8]["expect"]); wantp = eval(w["tests"][9]["expect"])
        check("short wealth expect equals the exact route", [round(float(x), 2) for x in wv] == want[1])
        check("short peak expect equals the exact route", [round(float(x), 2) for x in pk] == wantp)

# ---------- L3
it = item("plotting", "homework-3.json", "h-price-file-report")
w = it["widget"]; sol = w["solution"]
print("L3 h-price-file-report")
f, r = summary(w, sol, "shipped solution", "all"); check("L3 shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("L3 starter fails", len(f) > 0)
mine = r'''
import csv, io, math, statistics, datetime
import matplotlib.pyplot as plt
def report_figure(text, path):
    rows = {}
    for rec in csv.DictReader(io.StringIO(text)):
        rows[datetime.date.fromisoformat(rec["date"])] = float(rec["close"])
    days = sorted(rows)
    c = [rows[d] for d in days]
    rd, r = days[1:], [c[k] / c[k - 1] - 1 for k in range(1, len(c))]
    vd = rd[4:]; v = [statistics.stdev(r[k - 4:k + 1]) * math.sqrt(252) for k in range(4, len(r))]
    peak, dd = -math.inf, []
    for x in c:
        peak = max(peak, x); dd.append(x / peak - 1)
    k = min(range(len(dd)), key=lambda i: dd[i])
    fig, axes = plt.subplots(3, 1, sharex=True)
    axes[0].plot(rd, r); axes[1].plot(vd, v); axes[2].plot(days, dd)
    label = f"Max drawdown {100 * dd[k]:.1f}%"
    axes[2].annotate(label, xy=(days[k], dd[k]), xytext=(days[0], dd[k]), arrowprops={"arrowstyle": "->"})
    fig.suptitle(f"Volatility {100 * statistics.stdev(r) * math.sqrt(252):.1f}%, max drawdown {100 * dd[k]:.1f}%")
    fig.savefig(path, dpi=150)
    return fig, axes
'''
f, _ = summary(w, mine, "reader solution (csv, dates, loops, statistics.stdev)", "all"); check("L3 reader solution passes", f == [])
L3plants = [
    ("file order kept", [('.sort_index()  # one row a day', '  # one row a day')]),
    ("repeated day kept", [('df.drop_duplicates("date").set_index', 'df.set_index')]),
    ("both copies dropped", [('df.drop_duplicates("date")', 'df.drop_duplicates("date", keep=False)')]),
    ("duplicates judged by close", [('df.drop_duplicates("date")', 'df.drop_duplicates("close")')]),
    ("returns on the earlier date", [('rets = closes.pct_change().dropna()', 'rets = closes.pct_change().shift(-1).dropna()')]),
    ("population sd", [('vol = rets.rolling(5).std()', 'vol = rets.rolling(5).std(ddof=0)')]),
    ("times 252, not root 252", [('vol = rets.rolling(5).std() * np.sqrt(252)', 'vol = rets.rolling(5).std() * 252')]),
    ("window not full allowed", [('rets.rolling(5).std()', 'rets.rolling(5, min_periods=2).std()')]),
    ("drawdown from the overall top", [('dd = closes / closes.cummax() - 1', 'dd = closes / closes.max() - 1')]),
    ("arrow at the lowest close", [('t, mdd = dd.idxmin(), dd.min()', 't, mdd = closes.idxmin(), dd.min()')]),
    ("no shared x axis", [('plt.subplots(3, 1, sharex=True,', 'plt.subplots(3, 1,')]),
    ("default dpi", [('fig.savefig(path, dpi=150, bbox_inches="tight")', 'fig.savefig(path)')]),
    ("not saved", [('    fig.savefig(path, dpi=150, bbox_inches="tight")\n', '')]),
    ("title volatility from the last rolling value", [('fig.suptitle(f"Volatility {rets.std() * np.sqrt(252):.1%}', 'fig.suptitle(f"Volatility {vol.iloc[-1]:.1%}')]),
    ("label drawdown unsigned", [('f"Max drawdown {mdd:.1%}"', 'f"Max drawdown {-mdd:.1%}"')]),
    ("dates left as text", [(', parse_dates=["date"])', ')')]),
]
for name, pairs in L3plants:
    f, _ = summary(w, patched(sol, *pairs), "plant: " + name)
    check("L3 plant caught: " + name, len(f) > 0)
# format margins: how far each shown percentage is from a rounding boundary at one decimal
ns = {}; exec(w["prelude"], ns)
def exact_stats(text):
    rows = {}
    for rec in csv.DictReader(io.StringIO(text)):
        rows[rec["date"]] = F(rec["close"])
    c = [rows[d] for d in sorted(rows)]
    r = [c[k] / c[k - 1] - 1 for k in range(1, len(c))]
    m = sum(r) / len(r); var = sum((x - m) ** 2 for x in r) / (len(r) - 1)
    peak, mdd = c[0], F(0)
    for x in c:
        peak = max(peak, x); mdd = min(mdd, x / peak - 1)
    return math.sqrt(var * 252) * 100, float(mdd) * 100, len(r)
for name, text, want in (("vendor_file()", ns["vendor_file"](), ("45.2", "-10.5", 17)), ("price_file(7, 40)", ns["price_file"](7, 40), ("24.3", "-11.0", 39))):
    v, d, nr = exact_stats(text)
    mv, md = abs((v * 10) % 1 - 0.5), abs((abs(d) * 10) % 1 - 0.5)
    print(f"  {name}: volatility {v:.6f}%, max drawdown {d:.6f}%, {nr} returns; distance from a .05 boundary {mv / 10:.4f} and {md / 10:.4f} points")
    check(f"{name}: {want[0]}% and {want[1]}%, both over 0.001 points from a boundary", f"{v:.1f}" == want[0] and f"{d:.1f}" == want[1] and nr == want[2] and mv > 0.01 and md > 0.01)
print("failures:", bad)
sys.exit(1 if bad else 0)
