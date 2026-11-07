"""opt-dash L1 h-parity-fit: shipped solution, starter, a reader solution by another route and reader-planted bugs."""
import sys
from harness import item, summary, run

w = item("opt-dash", "homework-1.json", "h-parity-fit")["widget"]
base = w["solution"]

READER = '''
import math
def parity_fit(df_T, S, T):
    calls, puts = {}, {}
    for K, kind, b, a in zip(df_T["strike"], df_T["type"], df_T["bid"], df_T["ask"]):
        if b > 0:
            (calls if kind == "call" else puts)[float(K)] = (b + a) / 2
    ks = sorted(set(calls) & set(puts))
    nan = (math.nan, math.nan, math.nan)
    if len(ks) < 3:
        return nan
    ys = [calls[k] - puts[k] for k in ks]
    kb, yb = sum(ks) / len(ks), sum(ys) / len(ys)
    b = sum((k - kb) * (y - yb) for k, y in zip(ks, ys)) / sum((k - kb) ** 2 for k in ks)
    a = yb - b * kb
    D = -b
    if D <= 0 or a <= 0:
        return nan
    F = a / D
    r = -math.log(D) / T
    q = -math.log(a / S) / T          # D F = S exp(-q T)
    return F, r, q
'''

BUGS = {
    "line through the two end strikes": base.replace(
        "slope, icept = np.polyfit(K, (w[\"call\"] - w[\"put\"]).to_numpy(), 1)",
        "y = (w[\"call\"] - w[\"put\"]).to_numpy(); slope = (y[-1] - y[0]) / (K[-1] - K[0]); icept = y[0] - slope * K[0]"),
    "call at the ask, put at the bid": base.replace(
        "m = ((df_T[\"bid\"] + df_T[\"ask\"]) / 2).where(df_T[\"bid\"] > 0)",
        "m = df_T[\"ask\"].where(df_T[\"type\"] == \"call\", df_T[\"bid\"]).where(df_T[\"bid\"] > 0)"),
    "yield from simple growth": base.replace("q = r - log(F / S) / T", "q = r - (F / S - 1) / T"),
    "count strikes before dropping unpaired ones": base.replace(
        "w = w.reindex(columns=[\"call\", \"put\"]).dropna()                # strikes with both mids\n    if len(w) < 3:\n        return nan",
        "w = w.reindex(columns=[\"call\", \"put\"])\n    if len(w) < 3:\n        return nan\n    w = w.dropna()"),
    "NaN for a negative rate too (D above 1)": base.replace("if D <= 0 or icept <= 0:", "if D <= 0 or D >= 1 or icept <= 0:"),
}
bad = 0
print("opt-dash L1 h-parity-fit")
f, _ = summary(w, base, "shipped solution"); bad += bool(f)
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
f, _ = summary(w, READER, "reader dict pairing, closed-form OLS"); bad += bool(f)
for name, src in BUGS.items():
    assert src != base, name
    f, _ = summary(w, src, "bug: " + name)
    if name.startswith("NaN for a negative") or name.startswith("count strikes"):
        continue  # reported in the review
    bad += not f
bad += any(x[0] != "pass" for x in run(w, base, "examples"))
print("FAILURES:", bad)
sys.exit(1 if bad else 0)
