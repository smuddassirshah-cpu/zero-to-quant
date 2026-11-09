"""alpha homework-4 h-neutral-book: shipped solution, starter, a reader solution (row loops with
statistics.median, no pandas arithmetic) and reader-planted slips (none from the author's list), on every
example and test. Also checks the book is unique under the prose: no tie at the median is a float accident,
and the only places the spec could be read two ways (the median of an even count, the cash rule) give one book.
Venv Python, from this folder."""
import sys, math
from harness import item, run, summary

it = item("alpha", "homework-4.json", "h-neutral-book")
w = it["widget"]
bad = 0

READER = r'''
import math, statistics
import pandas as pd

def split_book(signal, gross):
    out = []
    for _, row in signal.iterrows():
        vals = [v for v in row.tolist() if not math.isnan(v)]
        pos = [0.0] * len(row)
        if vals:
            m = statistics.median(vals)
            d = [None if math.isnan(v) else v - m for v in row.tolist()]
            L = sum(x for x in d if x is not None and x > 0)
            S = -sum(x for x in d if x is not None and x < 0)
            if L > 0 and S > 0:
                for j, x in enumerate(d):
                    if x is None or x == 0:
                        continue
                    pos[j] = gross / 2 * (x / L if x > 0 else x / S)
        out.append(pos)
    return pd.DataFrame(out, index=signal.index, columns=signal.columns)

def split_pnl(signal, ret, gross):
    B = split_book(signal, gross)
    vals = []
    for i in range(1, len(B)):
        tot = 0.0
        for j, c in enumerate(B.columns):
            r = ret.iloc[i, j]
            tot += B.iloc[i - 1, j] * (0.0 if math.isnan(r) else r)
        vals.append(tot)
    return pd.Series(vals, index=B.index[1:])
'''

sol = w["solution"]
def slip(*pairs):
    s = sol
    for old, new in pairs:
        assert old in s, old
        s = s.replace(old, new)
    return s

SLIPS = {
    "NumPy median, a NaN spoils the row (cash)": slip(("signal.median(axis=1)", "pd.Series(signal.values.__array__().copy(), dtype=object).map(lambda r: r) if False else pd.Series(__import__('numpy').median(signal.values, axis=1), index=signal.index)")),
    "missing signal forward-filled": slip(("d = signal.sub(signal.median(axis=1), axis=0)", "signal = signal.ffill()\n    d = signal.sub(signal.median(axis=1), axis=0)")),
    "equal weights on each side": slip(("up, down = d.clip(lower=0), d.clip(upper=0)", "up, down = (d > 0).astype(float), -(d < 0).astype(float)")),
    "lower median of an even count": slip(("signal.median(axis=1)", "signal.apply(lambda r: __import__('statistics').median_low(r.dropna()) if r.notna().any() else float('nan'), axis=1)")),
    "weight by |signal|, sides split at the median": slip(("up, down = d.clip(lower=0), d.clip(upper=0)", "up, down = signal.abs().where(d > 0, 0.0), -signal.abs().where(d < 0, 0.0)")),
    "returns lagged as well as positions": slip(("(held * ret.fillna(0.0))", "(held * ret.shift(1).fillna(0.0))")),
    "cumulative P&L returned": slip(("return (held * ret.fillna(0.0)).sum(axis=1).iloc[1:]", "return (held * ret.fillna(0.0)).sum(axis=1).cumsum().iloc[1:]")),
}

print("h-neutral-book")
f, _ = summary(w, sol, "shipped solution"); bad += bool(f)
ex = run(w, sol, "examples"); bad += any(x[0] != "pass" for x in ex)
print("  examples pass:", all(x[0] == "pass" for x in ex))
f, _ = summary(w, READER, "reader solution (row loops)"); bad += bool(f)
bad += any(x[0] != "pass" for x in run(w, READER, "examples"))
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
for name, src in SLIPS.items():
    f, _ = summary(w, src, "slip: " + name)
    if not f:
        print("     ^ passes every test"); bad += 1

# Uniqueness: on every date of five_days() and panel(7), is any share within 1e-9 of the median but not equal
# (a float tie that two correct codings could split differently)? And is the median ever the mean of two
# different middles with a share equal to it (impossible, but checked)?
g = {}
exec(w["prelude"], g)
near = 0
for S, R in [g["five_days"](), g["panel"](7), g["panel"](11)]:
    med = S.median(axis=1)
    d = S.sub(med, axis=0)
    near += int(((d.abs() > 0) & (d.abs() < 1e-9)).sum().sum())
print("  shares within 1e-9 of the median but not on it:", near)
bad += near != 0

# The four example values recomputed by hand for 4 March: signals 0.9 0.3 -0.2 0.1 -0.6 0.5, median 0.2
m = (0.1 + 0.3) / 2
d = [0.9 - m, 0.3 - m, -0.2 - m, 0.1 - m, -0.6 - m, 0.5 - m]
L = sum(x for x in d if x > 0); S_ = -sum(x for x in d if x < 0)
book = [5e5 * (x / L if x > 0 else x / S_) for x in d]
want = [318181.82, 45454.55, -153846.15, -38461.54, -307692.31, 136363.64]
ok = all(abs(a - b) < 0.01 for a, b in zip(book, want))
print("  4 March by hand: L =", round(L, 4), "S =", round(S_, 4), "matches example:", ok)
bad += not ok
# explain: one scale leaves the book net short 1e6*(L - S)/(L + S)
net = 1e6 * (L - S_) / (L + S_)
print("  one-scale net exposure £", round(net, 2), "(explain says £83,333 net short)")
bad += abs(net + 83333.33) > 0.01
print("bad:", bad)
sys.exit(1 if bad else 0)
