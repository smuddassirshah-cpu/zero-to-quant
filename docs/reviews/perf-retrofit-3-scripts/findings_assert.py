"""Findings of review-perf-retrofit-3, one assertion each. Exits 1 by design until every fix lands:
each FAIL line names its finding. Also lists, for each longform rubric, every passing tick set
(7 of 10 or more, every required row ticked) and marks those that leave out a named part.
Venv Python, from this folder."""
import itertools, json, pathlib, re, sys
from harness import item, run, ROOT

fails = 0
def check(fid, ok, msg):
    global fails
    fails += not ok
    print(("ok   " if ok else "FAIL ") + f"{fid}: {msg}")

def rubric_of(it):
    return it.get("rubric") or it["widget"]["rubric"]

def passes(rub):
    out = []
    n = len(rub)
    for k in range(1, n + 1):
        for s in itertools.combinations(range(n), k):
            if sum(rub[i]["points"] for i in s) >= 7 and all(i in s for i in range(n) if rub[i].get("required")):
                out.append([i + 1 for i in s])
    return out

# named parts per item: rows (1-based) the objective or the task's question names
LONG = {
    ("ito", "homework-3.json", "h-derive-black"): {"assumptions": 1, "shares (hedge)": 3, "the equation": 4, "the check": 5},
    ("ito", "homework-4.json", "h-aloud-unknown-drift"): {"assumptions first": 1, "hedge with mu_t cancelling": 3, "the equation": 4},
    ("alpha", "homework-3.json", "h-overlap-aloud"): {"why t inflates": 2, "how much": 3, "what stays valid": 4, "what to report": 5},
}
print("Passing tick sets (rows 1-based); '<- skips' names a part the question or objective names")
skip_by = {}
for key, named in LONG.items():
    it = item(*key)
    rub = rubric_of(it)
    req = [i + 1 for i, r in enumerate(rub) if r.get("required")]
    print(f"  {key[2]}: points {[r['points'] for r in rub]}, required {req}")
    bad = []
    for s in passes(rub):
        miss = [p for p, row in named.items() if row not in s]
        if miss:
            bad.append(s)
        print(f"     {s}" + (f"  <- skips {', '.join(miss)}" if miss else ""))
    skip_by[key[2]] = bad

check("IT3-1", not skip_by["h-derive-black"], "ito L3: no pass may skip the equation, the assumptions or the check (required on rows 1, 3, 4, 5)")
check("IT4-1", not skip_by["h-aloud-unknown-drift"], "ito L4: no pass may skip the equation or the assumptions (required on rows 1, 3, 4)")
check("AL3-1", not skip_by["h-overlap-aloud"], "alpha L3: no pass may skip how much, what stays valid or what to report (required on rows 2, 3, 4, 5)")

# OD1-1 Must: least squares is not taught by opt-dash L1 or its gated chain; the prose must define it in place
od1 = item("opt-dash", "homework-1.json", "h-parity-fit")
check("OD1-1", "\\bar K" in od1["prose"] or "\\bar{K}" in od1["prose"], "opt-dash L1: the prose defines the least-squares slope and intercept, since no lesson by level 1 teaches least squares")

# AL3-2 Should: Newey-West with Bartlett weights at 62 lags still understates the variance (factor 42, not 63)
al3 = item("alpha", "homework-3.json", "h-overlap-aloud")
m = al3["widget"]["model"]
check("AL3-2", "at least 62" in m.lower() and "at least 62" in rubric_of(al3)[4]["text"].lower(),
      "alpha L3: follow-up (2) and rubric row 5 say at least 62 lags and that the weights shrink the far lags")

# AL1-1 Could: mean(close) * mean(shares) passes every test
w1 = item("alpha", "homework-1.json", "h-review-universe")["widget"]
bug = w1["solution"].replace("adv = gbp.rolling(window, min_periods=window).mean()",
                             "adv = close.rolling(window, min_periods=window).mean() * shares.rolling(window, min_periods=window).mean()")
r = run(w1, bug, "tests")
check("AL1-1", any(x[0] != "pass" for x in r), "alpha L1: a test fails the product of the mean close and the mean shares")
proposed = {"setup": "c, s, l = hand(); c.loc['2024-01-29':'2024-01-31', 'B'] = [1.0, 9.0, 1.0]; s.loc['2024-01-29':'2024-01-31', 'B'] = [4000.0, 400.0, 4000.0]",
            "call": "members(review_universe(c, s, l, 2, 3).loc[[\"2024-02-01\"]])", "expect": "['AD']", "compare": "equal"}
pw = dict(w1, examples=[], tests=[proposed])
print(f"     proposed test: solution {run(pw, w1['solution'], 'tests')[0][0]}, bug {run(pw, bug, 'tests')[0][0]}")

# OD1-2 Could: counting strikes before dropping unpaired ones passes every test
w2 = od1["widget"]
bug2 = w2["solution"].replace("w = w.reindex(columns=[\"call\", \"put\"]).dropna()                # strikes with both mids\n    if len(w) < 3:\n        return nan",
                              "w = w.reindex(columns=[\"call\", \"put\"])\n    if len(w) < 3:\n        return nan\n    w = w.dropna()")
bug3 = w2["solution"].replace("if D <= 0 or icept <= 0:", "if D <= 0 or D >= 1 or icept <= 0:")
check("OD1-2", any(x[0] != "pass" for x in run(w2, bug2, "tests")), "opt-dash L1: a test fails a solution that counts strikes, not pairs")
check("OD1-3", any(x[0] != "pass" for x in run(w2, bug3, "tests")), "opt-dash L1: a test fails a solution that returns NaN for a negative rate")
prop2 = {"call": "[v != v for v in parity_fit(without(without(toy_chain(100, 0.04, 0.01, 0.25, 1.0, [90, 95, 100, 105]), 90, 'put'), 105, 'call'), 100, 1.0)]", "expect": "[True, True, True]", "compare": "equal"}
prop3 = {"call": "list(parity_fit(toy_chain(100, -0.01, 0.0, 0.25, 1.0, range(80, 121, 5)), 100, 1.0))", "expect": "[100 * exp(-0.01), -0.01, 0.0]", "compare": "isclose", "tol": {"abs": 1e-09}}
for nm, pt, b in (("pairs", prop2, bug2), ("negative rate", prop3, bug3)):
    pw = dict(w2, examples=[], tests=[pt])
    print(f"     proposed {nm} test: solution {run(pw, w2['solution'], 'tests')[0][0]}, bug {run(pw, b, 'tests')[0][0]}")

# IT3-2 Could: the report says the forward is taught in l16 (level 4); ito l8 screen 10 (level 2) teaches it
rep3 = (ROOT / "docs/reports/ito-3-perf.md").read_text()
check("IT3-2", "taught in l16" not in rep3 and "l8" in rep3, "ito L3 report: cites l8 screen 10 for the forward price, not l16")

# IT3-3 Could: the prompt says share and cash; the model's book holds no cash
it3 = item("ito", "homework-3.json", "h-derive-black")
check("IT3-3", "C = V - \\Delta S" in it3["model"], "ito L3: the model says where the cash is, as the prompt asks for share and cash")

# IT3-4 Could: step 8's display ends with a comma before a new sentence
check("IT3-4", "- rV, \\end{aligned}$$\nThe right side" not in it3["model"],
      "ito L3: step 8's display ends with a full stop")

# IT4-2 Could: rubric row 1 says mu_t 'otherwise free' though the model needs it integrable
it4 = item("ito", "homework-4.json", "h-aloud-unknown-drift")
check("IT4-2", "integrable" in rubric_of(it4)[0]["text"], "ito L4: rubric row 1 asks for mu_t adapted and integrable")
# IT4-3 Could: no arbitrage limits mu_t too
check("IT4-3", "(\\mu_t - r)^2" in it4["model"], "ito L4: the model says no arbitrage is also a condition on mu_t")

# RPT Could: reports name the lesson screens that lay out the product
need = {"ito-3": ["l9 screen 2"], "ito-4": ["l17 screen"], "alpha-1": ["l1 screens 6"], "alpha-2": ["l5 screen 4", "l7 screen 4"]}
for rep, terms in need.items():
    t = (ROOT / f"docs/reports/{rep}-perf.md").read_text()
    check("RPT", all(x in t for x in terms), f"report {rep} names {', '.join(terms)}")

print("FAILS:", fails)
sys.exit(1 if fails else 0)
