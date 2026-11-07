"""alpha L1 h-review-universe: shipped solution, starter, a reader solution by another route and reader-planted bugs."""
import sys
from harness import item, summary, run

it = item("alpha", "homework-1.json", "h-review-universe")
w = it["widget"]

READER = '''
import pandas as pd
def review_universe(close, shares, listed, n, window):
    dates = list(close.index)
    cols = list(close.columns)
    out = pd.DataFrame(False, index=close.index, columns=close.columns)
    current = []
    for i, d in enumerate(dates):
        # membership today: the list chosen at the last review before today
        for c in current:
            if bool(listed.at[d, c]):
                out.at[d, c] = True
        last_of_month = i + 1 == len(dates) or dates[i + 1].month != d.month or dates[i + 1].year != d.year
        if last_of_month and i + 1 >= window:
            cand = []
            for c in cols:
                if not bool(listed.at[d, c]):
                    continue
                vals = []
                for j in range(i - window + 1, i + 1):
                    v = close.iat[j, cols.index(c)] * shares.iat[j, cols.index(c)]
                    if v != v:
                        break
                    vals.append(v)
                if len(vals) == window:
                    cand.append((-sum(vals) / window, c))
            current = [c for _, c in sorted(cand)[:n]]
        elif last_of_month:
            current = []
    return out
'''

base = w["solution"]
BUGS = {
    "product of the means, not mean of the product": base.replace(
        'adv = gbp.rolling(window, min_periods=window).mean()',
        'adv = close.rolling(window, min_periods=window).mean() * shares.rolling(window, min_periods=window).mean()'),
    "review on each month's first trading day": base.replace('keep="last"', 'keep="first"'),
    "list held to the day before the next review": base.replace(
        'close.index <= reviews[k + 1]', 'close.index < reviews[k + 1]'),
    "window in calendar days": base.replace(
        'gbp.rolling(window, min_periods=window)', 'gbp.rolling(f"{window}D")'),
    "unstable sort (no mergesort, no sort_index)": base.replace(
        '.dropna().sort_index()', '.dropna()').replace(', kind="mergesort"', ''),
    "eligibility on any listed day in the window": base.replace(
        'gbp.rolling(window, min_periods=window)', 'gbp.rolling(window, min_periods=1)'),
}

bad = 0
print("alpha L1 h-review-universe")
f, _ = summary(w, base, "shipped solution")
bad += bool(f)
f, _ = summary(w, w["starter"], "starter")
bad += len(f) != len(w["tests"])
f, _ = summary(w, READER, "reader day-loop solution")
bad += bool(f)
for name, src in BUGS.items():
    assert src != base, name
    f, _ = summary(w, src, "bug: " + name)
    if name.startswith("unstable") or name.startswith("product"):
        continue  # unstable sort: still correct here; product of means: finding AL1-1, asserted in findings_assert.py
    bad += not f
ex = run(w, base, "examples")
bad += any(x[0] != "pass" for x in ex)
print("FAILURES:", bad)
sys.exit(1 if bad else 0)
