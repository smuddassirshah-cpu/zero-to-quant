"""alpha L2 h-momentum-pct: shipped solution, starter, a reader solution by another route and reader-planted bugs."""
import sys
from harness import item, summary, run

w = item("alpha", "homework-2.json", "h-momentum-pct")["widget"]
base = w["solution"]

READER = '''
import math
import pandas as pd
def momentum_pct(px, lookback=12, skip=1):
    out = pd.DataFrame(float("nan"), index=px.index, columns=px.columns)
    for t in range(len(px)):
        if t - lookback < 0:
            continue
        sc = {}
        for c in px.columns:
            now, a, b = px[c].iloc[t], px[c].iloc[t - lookback], px[c].iloc[t - skip]
            if not (math.isnan(now) or math.isnan(a) or math.isnan(b)):
                sc[c] = math.log(b) - math.log(a)        # log return: same order as the simple return
        n = len(sc)
        for c, v in sc.items():
            below = sum(1 for x in sc.values() if x < v)
            same = sum(1 for x in sc.values() if x == v)
            out.at[px.index[t], c] = (below + (same + 1) / 2) / n
    return out
'''

BUGS = {
    "ties take the lowest rank": base.replace("rank(axis=1, pct=True)", "rank(axis=1, pct=True, method='min')"),
    "divide by the shares listed at t, not those scored": base.replace(
        "return mom.rank(axis=1, pct=True)", "return mom.rank(axis=1).div(px.notna().sum(axis=1), axis=0)"),
    "lookback counted back from t - skip": base.replace("px.shift(lookback)", "px.shift(lookback + skip)"),
    "listed at every month of the window (stricter than the rule)": base.replace(
        "mom = mom.where(px.notna())", "mom = mom.where(px.notna() & px.notna().astype(float).rolling(lookback + 1).min().eq(1))"),
}
bad = 0
print("alpha L2 h-momentum-pct")
f, _ = summary(w, base, "shipped solution"); bad += bool(f)
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
f, _ = summary(w, READER, "reader loop, log returns, hand average rank"); bad += bool(f)
for name, src in BUGS.items():
    assert src != base, name
    f, _ = summary(w, src, "bug: " + name)
    if name.startswith("listed at every"):
        continue  # no test panel has a gap inside a window; reported only
    bad += not f
bad += any(x[0] != "pass" for x in run(w, base, "examples"))
print("FAILURES:", bad)
sys.exit(1 if bad else 0)
