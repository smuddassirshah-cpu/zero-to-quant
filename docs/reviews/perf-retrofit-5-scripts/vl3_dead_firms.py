"""validation homework-3 h-dead-firms: shipped solution, starter, a reader solution (a month loop over
listing records in a dict) and reader-planted slips, on every example and test. Venv Python, from this folder."""
import sys
from harness import item, run, summary

it = item("validation", "homework-3.json", "h-dead-firms")
w = it["widget"]
bad = 0
READER = r'''
import math
import pandas as pd

def survivor_free_returns(rets, listings, delist):
    rec = {f: (a, b) for f, a, b in listings}
    held, ret = [], []
    for m in rets.index:
        rs = []
        for f, (a, b) in rec.items():
            if m < a or (b is not None and m > b):
                continue
            x = rets.at[m, f] if f in rets.columns else float("nan")
            if b == m:
                x = (1 + (0.0 if x != x else x)) * (1 + delist[f]) - 1
            rs.append(x)
        held.append(len(rs))
        ret.append(sum(rs) / len(rs) if rs else float("nan"))
    return pd.DataFrame({"held": held, "ret": ret}, index=rets.index)
'''
sol = w["solution"]
def slip(old, new):
    assert old in sol, old
    return sol.replace(old, new)
SLIPS = {
    "delisting return added, not compounded": slip("r.loc[last, firm] = (1 + base) * (1 + delist[firm]) - 1", "r.loc[last, firm] = base + delist[firm]"),
    "dead firm left out of its last month": slip("(months <= last)", "(months < last)"),
    "held counted from firms with a return": slip('"held": held.sum(axis=1)', '"held": (held & rets.notna()).sum(axis=1)'),
    "missing regular return skipped, so no delisting return": slip("base = 0.0 if np.isnan(base) else base", "pass"),
    "delisting return a month late": slip("if last in months:", "if False:"),
    "mean over the listed with a return only, delist on next month": slip("r.loc[last, firm] = (1 + base) * (1 + delist[firm]) - 1", "r.loc[last, firm] = base"),
}
print("h-dead-firms")
f, _ = summary(w, sol, "shipped solution"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, sol, "examples"))
f, _ = summary(w, READER, "reader solution (month loop)"); bad += bool(f)
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
for name, src in SLIPS.items():
    f, _ = summary(w, src, "slip: " + name)
    if not f:
        print("     ^ passes every test"); bad += 1
print("bad:", bad)
sys.exit(1 if bad else 0)
