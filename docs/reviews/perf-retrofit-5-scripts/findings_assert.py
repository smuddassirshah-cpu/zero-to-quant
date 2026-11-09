"""Findings of review-perf-retrofit-5, one assertion each. Exits 1 by design until every fix lands:
each FAIL line names its finding. Also lists, for each longform rubric, every passing tick set
(7 of 10 or more, every required row ticked) and marks those that leave out a named part.
Venv Python, from this folder."""
import itertools, pathlib, sys
from fractions import Fraction as F
from itertools import product
from harness import item, run, ROOT

fails = 0
def check(fid, ok, msg):
    global fails
    fails += not ok
    print(("ok   " if ok else "FAIL ") + f"{fid}: {msg}")

def field(it, k):
    return it[k] if k in it else it["widget"][k]

def passes(rub):
    n = len(rub)
    return [[i + 1 for i in s] for k in range(1, n + 1) for s in itertools.combinations(range(n), k)
            if sum(rub[i]["points"] for i in s) >= 7 and all(i in s for i in range(n) if rub[i].get("required"))]

LONG = {  # rows (1-based) for each part the objective or the task's question names
    ("coint", "homework-1.json", "h-spurious-aloud"): {"conditions": 1, "why t misleads and grows": 2, "why R^2 misleads": 3, "what to run instead": 4},
    ("mm-games", "homework-3.json", "h-coin-dice-aloud"): {"each quote with fair value": 1, "why it moved": 2, "why that wide": 3, "position and P&L after each trade": 4},
    ("momentum-rep", "homework-1.json", "h-ivol-plan"): {"data and traps": 1, "steps in order": 2, "checks for each trap": 3},
}
skip = {}
print("Passing tick sets (rows 1-based); '<- skips' names a part the question or objective names")
for key, named in LONG.items():
    rub = field(item(*key), "rubric")
    print(f"  {key[2]}: points {[r['points'] for r in rub]}, required {[i + 1 for i, r in enumerate(rub) if r.get('required')]}")
    skip[key[2]] = []
    for s in passes(rub):
        miss = [p for p, row in named.items() if row not in s]
        if miss: skip[key[2]].append(s)
        print(f"     {s}" + (f"  <- skips {', '.join(miss)}" if miss else ""))
check("MG3-2", not skip["h-coin-dice-aloud"], "mm-games L3: no pass may skip position and P&L, which the prompt names (required on row 4)")
check("clean", not skip["h-spurious-aloud"] and not skip["h-ivol-plan"], "coint L1 and momentum-rep L1: no pass skips a named part")

# MG3-1 Must: the mixed total is not two-humped with little mass near 10.5
def dice(k):
    d = {}
    for r in product(range(1, 7), repeat=k):
        d[sum(r)] = d.get(sum(r), 0) + F(1, 6 ** k)
    return d
two, four = dice(2), dice(4)
mix = lambda s: (two.get(s, 0) + four.get(s, 0)) / 2
print(f"  fact: P(total = 10) = {float(mix(10)):.4f} > P(total = 14) = {float(mix(14)):.4f}; P(9 to 12) = {float(sum(mix(s) for s in range(9, 13))):.3f}")
mm = item("mm-games", "homework-3.json", "h-coin-dice-aloud")
txt = field(mm, "model") + " " + field(mm, "rubric")[2]["text"]
check("MG3-1", "rarely near 10.5" not in txt and "lands near 7 or near 14" not in txt,
      "mm-games L3: model and rubric row 3 no longer say the total lands near 7 or 14 and rarely near 10.5")
rep = (ROOT / "docs" / "reports" / "mm-games-3-perf.md").read_text()
check("MG3-3", "two-humped" not in rep, "mm-games L3 report: no 'two-humped total'")

# coint L1
co = field(item("coint", "homework-1.json", "h-spurious-aloud"), "model")
fu1 = co[co.index("(1)"):co.index("(2)")]
fu2 = co[co.index("(2)"):co.index("(3)")]
check("COI-1", "seeded" in fu1 and "seeded run" in co[co.index("never settles"):co.index("never settles") + 160],
      "coint L1: the drift figures and the slope's spread each name the seeded run they come from")
check("COI-2", "\\phi^{|k|}" in fu2 and "n^2" in fu2, "coint L1: follow-up (2) justifies the 1/n error and the long-run variance from the AR(1) autocovariances")
check("COI-3", "I(1): each is a random walk" not in co, "coint L1: I(1) is not equated with a random walk")

# VL3-1: a listing record that ends after the file
w = item("validation", "homework-3.json", "h-dead-firms")["widget"]
clip = w["solution"].replace("        if last in months:", "        last = min(last, months[-1]) if last else last\n        if last in months:")
r = run(w, clip, "tests")
check("VL3-1", any(x[0] != "pass" for x in r), "validation L3: a solution that clips a record's last month into the file fails a test")

# momentum-rep L1
mo = field(item("momentum-rep", "homework-1.json", "h-ivol-plan"), "model")
check("MOM-3", "January 1973" in mo, "momentum-rep L1: the Nasdaq check says scored Nasdaq shares first appear at the end of January 1973 under the 15-day rule")
check("MOM-4", "450" in mo or "August 1963" in mo, "momentum-rep L1: the model says which months the 449 holding months are")
mrep = (ROOT / "docs" / "reports" / "momentum-rep-1-perf.md").read_text()
check("MOM-2", "w10852" in mrep and "14 December 1972" in mrep, "momentum-rep L1 report: names the sources for -1.06% and the Nasdaq start")
print("FAILS:", fails)
sys.exit(1 if fails else 0)
