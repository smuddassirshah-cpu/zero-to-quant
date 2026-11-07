"""opt-dash L3 h-black-iv: shipped solution, starter, a reader solution by another route and reader-planted bugs,
including the two the orchestrator named: a number at or outside the bounds, and an exception there."""
import sys
from harness import item, summary, run

w = item("opt-dash", "homework-3.json", "h-black-iv")["widget"]
base = w["solution"]

READER = '''
from math import erf, exp, log, sqrt, nan, isnan
def _N(z):
    return 0.5 * (1 + erf(z / sqrt(2)))
def _px(F, K, D, s, T, kind):
    v = s * sqrt(T); d1 = log(F / K) / v + v / 2; d2 = d1 - v
    c = D * (F * _N(d1) - K * _N(d2))
    return c if kind == "call" else c - D * (F - K)      # put by parity
def black_iv(price, F, K, D, T, kind="call"):
    if kind not in ("call", "put"):
        raise ValueError(kind)
    if isnan(price):
        return nan
    lo_b = D * max((F - K) if kind == "call" else (K - F), 0.0)
    hi_b = D * (F if kind == "call" else K)
    if price <= lo_b or price >= hi_b:
        return nan
    a, b = log(1e-6), log(20.0)                         # bisection in log vol only
    for _ in range(200):
        m = (a + b) / 2
        if _px(F, K, D, exp(m), T, kind) > price:
            b = m
        else:
            a = m
        if b - a < 1e-14:
            break
    return exp((a + b) / 2)
'''

def edit(old, new):
    assert old in base, old
    return base.replace(old, new)

BUGS = {
    "a number (0.0) at or outside the bounds": edit("if not lower < price < upper:          # also False for a NaN price\n        return nan",
                                                   "if not lower < price < upper:\n        return 0.0"),
    "raises ValueError at or outside the bounds": edit("if not lower < price < upper:          # also False for a NaN price\n        return nan",
                                                      "if not lower < price < upper:\n        raise ValueError('no vol')"),
    "None at or outside the bounds": edit("if not lower < price < upper:          # also False for a NaN price\n        return nan",
                                         "if not lower < price < upper:\n        return None"),
    "bounds checked with <= (edge prices solved)": edit("if not lower < price < upper:", "if price != price or not lower <= price <= upper:"),
    "search capped at 200%": edit("if hi > 1000:", "if hi > 2:"),
    "stops at a price error of 1e-6": edit("if abs(diff) < 1e-13:", "if abs(diff) < 1e-6:"),
    "any kind not 'call' priced as a put": edit("    else:\n        raise ValueError(\"kind must be 'call' or 'put'\")\n", "    else:\n        lower, upper = D * max(K - F, 0.0), D * K\n").replace('if kind == "call":\n        return D * (F', 'if kind == "call":\n        return D * (F'),
}
VARIANTS = {
    "bisection that stops at a price error of 1e-8 (the prose's tolerance)": READER.replace(
        "        if b - a < 1e-14:\n            break", "        if abs(_px(F, K, D, exp((a + b) / 2), T, kind) - price) < 1e-8:\n            break"),
}
bad = 0
print("opt-dash L3 h-black-iv")
f, _ = summary(w, base, "shipped solution"); bad += bool(f)
f, _ = summary(w, w["starter"], "starter"); bad += len(f) != len(w["tests"])
f, _ = summary(w, READER, "reader log-vol bisection, put by parity"); bad += bool(f)
for name, src in VARIANTS.items():
    f, _ = summary(w, src, "variant: " + name); bad += bool(f)
for name, src in BUGS.items():
    assert src != base, name
    f, _ = summary(w, src, "bug: " + name); bad += not f
bad += any(x[0] != "pass" for x in run(w, base, "examples"))
print("FAILURES:", bad)
sys.exit(1 if bad else 0)
