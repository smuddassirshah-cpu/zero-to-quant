"""validation homework-2 h-label-purge: shipped solution, starter, a reader solution by another route
(explicit loops over positions and sets of return days), and reader-planted slips, on every example and test.
Venv Python, from this folder. Exits 1 on any unexpected result."""
import sys
from harness import item, run, summary

it = item("validation", "homework-2.json", "h-label-purge")
w = it["widget"]
bad = 0

READER = r'''
import numpy as np
import pandas as pd

def label_table(px, h):
    a = px.to_numpy(dtype=float)
    out = np.full(a.shape, np.nan)
    n = a.shape[0]
    for t in range(n):
        if t + h >= n:
            continue
        for j in range(a.shape[1]):
            p0, p1 = a[t, j], a[t + h, j]
            if p0 == p0 and p1 == p1:
                out[t, j] = p1 / p0 - 1
    return pd.DataFrame(out, index=px.index, columns=px.columns)

def train_dates(px, h, test_start, test_end):
    idx = list(px.index)
    s = idx.index(pd.Timestamp(test_start)); e = idx.index(pd.Timestamp(test_end))
    fold_days = set()
    for t in range(s, e + 1):
        fold_days |= set(range(t + 1, t + h + 1))
    lab = label_table(px, h)
    keep = []
    for t in range(len(idx)):
        if s <= t <= e:
            continue
        if set(range(t + 1, t + h + 1)) & fold_days:
            continue
        if lab.iloc[t].notna().any():
            keep.append(idx[t])
    return keep
'''

sol = w["solution"]
def slip(old, new):
    assert old in sol, old
    return sol.replace(old, new)

SLIPS = {
    # reader-planted, none from the author's list of 17 as written there
    "label by log return": slip("return px.shift(-h) / px - 1", "return np.log(px.shift(-h) / px)"),
    "purge with < instead of <= (one extra date lost before)": slip("(pos <= s - h)", "(pos < s - h)"),
    "purge after the fold only from e + h + 1": slip("(pos >= e + h)", "(pos > e + h)"),
    "labelled = every share has a label (all, not any)": slip(".notna().any(axis=1)", ".notna().all(axis=1)"),
    "test_end exclusive": slip("e = px.index.get_loc(pd.Timestamp(test_end))", "e = px.index.get_loc(pd.Timestamp(test_end)) - 1"),
    "label from close t-h to t, put on t + h then shifted back by h-1": slip("return px.shift(-h) / px - 1", "return (px / px.shift(h) - 1).shift(-(h - 1))"),
    "pct_change with ffill of halts": slip("return px.shift(-h) / px - 1", "return px.ffill().pct_change(h).shift(-h).where(px.notna())"),
}

print("h-label-purge")
f, r = summary(w, sol, "shipped solution")
bad += bool(f)
ex = run(w, sol, "examples"); bad += any(x[0] != "pass" for x in ex)
f, _ = summary(w, READER, "reader solution (loops and day sets)")
bad += bool(f)
f, _ = summary(w, w["starter"], "starter")
bad += len(f) != len(w["tests"])
for name, src in SLIPS.items():
    f, _ = summary(w, src, "slip: " + name)
    if not f:
        print("     ^ passes every test"); bad += 1
# Ambiguity probe: purge by the fold's labels that exist (per share) instead of by rows
PER_SHARE = READER.replace("        if set(range(t + 1, t + h + 1)) & fold_days:\n            continue\n",
"""        lt = lab.iloc[t]
        clash = False
        for c in px.columns:
            if lt[c] != lt[c]:
                continue
            fd = set()
            for u in range(s, e + 1):
                if lab.iloc[u][c] == lab.iloc[u][c]:
                    fd |= set(range(u + 1, u + h + 1))
            if set(range(t + 1, t + h + 1)) & fd:
                clash = True
        if clash:
            continue
""")
f, _ = summary(w, PER_SHARE, "reading: purge per share, by labels that exist")
bad += bool(f)  # a second reasonable reading of the prose must also pass
print("bad:", bad)
sys.exit(1 if bad else 0)
