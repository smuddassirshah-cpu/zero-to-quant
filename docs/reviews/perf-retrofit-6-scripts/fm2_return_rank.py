"""fin-ml homework-2 h-return-rank: shipped solution, starter, a reader solution (dicts by share and date,
no pandas groupby, ranks by hand) and reader-planted slips (none from the author's list), on every example
and test. Also probes whether a look-back in business days, not in the table's dates, is told apart.
Venv Python, from this folder."""
import sys
from harness import item, run, summary

it = item("fin-ml", "homework-2.json", "h-return-rank")
w = it["widget"]
bad = 0

READER = r'''
import math
import pandas as pd

def return_rank(df, k):
    dates = sorted(set(df["date"]))
    pos = {d: i for i, d in enumerate(dates)}
    close = {}
    for d, s, c in zip(df["date"], df["stock"], df["close"]):
        close[(s, pos[d])] = c
    feat = {}
    for (s, i), c in close.items():
        if i - k >= 0 and (s, i - k) in close:
            c0 = close[(s, i - k)]
            if not (math.isnan(c) or math.isnan(c0)):
                feat[(s, i)] = c / c0 - 1
    score = {}
    for i in range(len(dates)):
        xs = sorted((v, s) for (s, j), v in feat.items() if j == i)
        n = len(xs)
        if n == 1:
            score[(xs[0][1], i)] = 0.0
            continue
        a = 0
        while a < n:
            b = a
            while b + 1 < n and xs[b + 1][0] == xs[a][0]:
                b += 1
            avg = (a + b) / 2 + 1
            for t in range(a, b + 1):
                score[(xs[t][1], i)] = 2 * (avg - 1) / (n - 1) - 1
            a = b + 1
    vals = [score.get((s, pos[d]), float("nan")) for d, s in zip(df["date"], df["stock"])]
    return pd.Series(vals, index=df.index)
'''

sol = w["solution"]
def slip(*pairs):
    s = sol
    for old, new in pairs:
        assert old in s, old
        s = s.replace(old, new)
    return s

SLIPS = {
    "missing closes dropped, then k closes back": slip(('s = df.sort_values("date")', 's = df.sort_values("date").dropna(subset=["close"])')),
    "returns min-max scaled, not ranked": slip(('q = 2 * (g.rank() - 1) / (n - 1) - 1', 'q = 2 * (r - g.transform("min")) / (g.transform("max") - g.transform("min")) - 1')),
    "scipy rankdata on each date with the NaNs in": slip(('q = 2 * (g.rank() - 1) / (n - 1) - 1',
        'from scipy.stats import rankdata\n    rk = r.groupby(s["date"]).transform(lambda v: pd.Series(rankdata(v.values), index=v.index))\n    q = 2 * (rk - 1) / (n - 1) - 1')),
    "NaN ranked last and counted": slip(('q = 2 * (g.rank() - 1) / (n - 1) - 1', 'q = 2 * (g.rank(na_option="bottom") - 1) / (g.transform("size") - 1) - 1')),
}
# A look-back by business-day offset, not by the table's dates: correct only while the table has no holiday.
BDAY = slip(('past = s.groupby("stock")["close"].shift(k)        # the close k dates before',
             'idx = s.set_index(["date", "stock"])["close"]\n    key = pd.MultiIndex.from_arrays([s["date"] - pd.offsets.BDay(k), s["stock"]])\n    past = pd.Series(idx.reindex(key).values, index=s.index)'))

print("h-return-rank")
f, _ = summary(w, sol, "shipped solution"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, sol, "examples"))
f, _ = summary(w, READER, "reader solution (dict loops)"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, READER, "examples"))
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
for name, src in SLIPS.items():
    f, _ = summary(w, src, "slip: " + name)
    if not f:
        print("     ^ passes every test"); bad += 1
f, _ = summary(w, BDAY, "probe: k business days by offset (FM2-1)")
if not f:
    print("     ^ passes every test: no table skips a business day")

# The proposed extra test (FM2-1): drop one whole business day from toy(), as a holiday.
HOL = {"setup": "df = toy(); df = df[df['date'] != df['date'].unique()[2]].reset_index(drop=True)",
       "call": "[day(return_rank(df, 1), df, i) for i in range(4)]", "compare": "equal"}
g = {}
exec(w["prelude"], g); exec(sol, g)
exec(HOL["setup"], g)
want = repr(eval(HOL["call"], g))
print("  holiday test expect:", want)
HOL["expect"] = want
w2 = dict(w); w2["tests"] = w["tests"] + [HOL]; w2["examples"] = []
for label, src, should in [("shipped", sol, True), ("reader", READER, True), ("bday probe", BDAY, False)]:
    r = run(w2, src, "tests")[-1]
    ok = (r[0] == "pass") == should
    print(f"  holiday test, {label}: {r[0]}  ({'as wanted' if ok else 'NOT as wanted'})")
    bad += not ok
print("bad:", bad)
sys.exit(1 if bad else 0)
